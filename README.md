# AI 小镇 (llm_town)

一个类似《模拟人生》的交互式沙盒游戏，名称叫AI小镇。游戏中有25个代理人，这些代理人由生成式智能体实例化，使用自然语言与最终用户进行交互。

游戏中场景包括 Lin家的房子、约翰逊公园、哈维橡木供应店、威洛斯市场和药店、霍布斯咖啡馆和玫瑰与皇冠酒吧等。

## 目录结构

    llm_town/
    ├── contracts/
    ├── client/
    ├── ai/
    ├── .gitignore
    ├── LICENSE
    └── README.md

## 环境要求

- Golang 1.16+
- Mud1 v1.39.0
- Node.js 18+
- Python 3.7+
- Docker

## 安装与运行

1. 克隆项目到本地：

        git clone https://github.com/fisherOu/llm_town.git

2. 进入项目目录：

        cd llm_town
        git submodule init
        git submodule update

3. 安装依赖（确保已安装相关环境要求）：


构建客户端服务镜像

    make build

4. 开始运行项目：

运行节点和客户端服务

    make start

部署合约到本地节点
    
    cd contracts && yarn dev


## 贡献

欢迎提交 PR 和 Issue 进行改进和补充项目内容。感谢您的参与！

## 许可

本项目采用 [MIT License](./LICENSE)。