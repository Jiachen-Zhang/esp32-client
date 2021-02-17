package main

import (
	"fmt"
	"log"
	"testing"
	"time"
)

func consumeString (stringChannel <-chan string) {
	for {
		s := <- stringChannel
		fmt.Printf("%s\n", s)
	}
}

func TestSendData(t *testing.T) {
	c := InitDialConnection()
	defer c.Close()
	stringChannel := make(chan string, 1024)

	go func() {
		for {
			time.Sleep(1 * time.Second)
			stringChannel <- time.Now().String()
		}
	}()
	log.Println("start send data")
	SendData(stringChannel, c)
}
