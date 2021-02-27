# esp32-client

[![build](https://github.com/Jiachen-Zhang/esp32_client/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/Jiachen-Zhang/esp32_client/actions/workflows/build.yml)

## 运行项目

1. 创建虚拟环境: `python3 -m venv venv`

2. 激活虚拟环境: `source venv/bin/activate`

3. 安装依赖: `pip install -r ./requirements.txt`

## 开发

1. 克隆项目

2. 使用虚拟环境

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirment.txt
```

3. 执行提交前代码检查

```shell
pylint esp32_client
```

4. \[Optional\] 执行 github action
    
    - 配置本地运行环境: `brew install nektos/tap/act` [reference](https://www.ctolib.com/nektos-act.html)
    - 运行 github workflow: `act`
