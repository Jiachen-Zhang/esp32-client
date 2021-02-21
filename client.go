// Copyright 2015 The Gorilla WebSocket Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package main

import (
	"bytes"
	"flag"
	"fmt"
	"github.com/gorilla/websocket"
	"github.com/tarm/serial"
	"log"
	"net/url"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"time"
)

func GetEnvOrDefault(name string, defaultValue string) string {
	value := os.Getenv(name)
	if value == "" {value = defaultValue }
	fmt.Println(value)
	return value
}

var u = url.URL{Scheme: "ws",
	Host: *flag.String("addr", "localhost:8080", "http service address"),
	Path: "/echo"}

// 将串口数据逐字节写入channel
func produceSerial(ch chan<- byte) {
	serialPort := GetEnvOrDefault("SERIAL_PORT", "/dev/tty.usbserial-0001")
	c := &serial.Config{Name: serialPort, Baud: 115200}
	s, err := serial.OpenPort(c)
	if err != nil { log.Fatal(err) }
	err = s.Flush()
	if err != nil { log.Fatal(err) }
	for {
		buf := make([]byte, 1024)
		n, err := s.Read(buf)
		if err != nil {
			log.Fatal(err)
		}
		for i, b := range buf {
			if i == n { break }
			ch <- b
		}
	}
}

// 从 byte channel 中读取数据拼接完整的 string 并写入 channel
func consumerByte(byteChannel <-chan byte, stringChannel chan<- string) {
	buf := bytes.NewBufferString("")
	for {
		b := <- byteChannel
		buf.WriteByte(b)
		if b == '\r' { continue }
		if b == '\n' {
			line := buf.String()
			buf.Reset()
			line = strings.TrimSpace(line)
			line += ", " + strconv.FormatInt(time.Now().UnixNano() / 1000000, 10)
			log.Printf("Assembly: %s", line)
			stringChannel <- line
		}
	}
}

func dialWebsocketConnection() *websocket.Conn {
	flag.Parse()
	log.SetFlags(0)
	log.Printf("connecting to %s", u.String())
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Println("dial:", err)
		time.Sleep(1 * time.Second)
		c, _, err = websocket.DefaultDialer.Dial(u.String(), nil)
	}
	return c
}

func main() {
	// disable log
	//log.SetOutput(ioutil.Discard)
	c := InitDialConnection()
	// serial communication
	byteChannel := make(chan byte, 1024)
	stringChannel := make(chan string, 1024)

	go produceSerial(byteChannel)
	go consumerByte(byteChannel, stringChannel)
	// websocket communication
	SendData(stringChannel, c)
}

// 从 string channel 读取数据发送给 ws server
func SendData(stringChannel <-chan string, c *websocket.Conn) {
	defer c.Close()
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	for {
		select {
		case s := <-stringChannel:
			if c == nil {
				log.Println("Invalid Connection")
				c = dialWebsocketConnection()
				break 	// drop this data, or use `continue` to block
			}
			log.Printf("Start to send %s\n", s)
			err := c.WriteMessage(websocket.TextMessage, []byte(s))
			if err != nil {
				log.Println("write:", err)
				c = dialWebsocketConnection()
			}
		case <-interrupt:
			log.Println("interrupt")

			// Cleanly close the connection by sending a close message and then
			// waiting (with timeout) for the server to close the connection.
			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Println("write close:", err)
				return
			}
			select {
			case <-time.After(time.Second):
			}
			return
		}
	}
}

func InitDialConnection() *websocket.Conn {
	c := dialWebsocketConnection()
	for {
		if c != nil {
			break
		} else {
			c = dialWebsocketConnection()
		}
	}
	return c
}
