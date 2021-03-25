function FrontendClient(url) {
    // 定義物件參數
    this.className = 'EWS_Frontend_Client';
    this.webSocketUrl = url;
    this.webSocket = null;
    this.isConnected = false;
    this.isLogin = false;
    this.serverStatus = false;
    this.clientId = null;

    // Interfaces
    this.userAuthCompletes = function () { };
    this.userAuthError = function () { };
    this.processMessage = function (payload) { };
    this.isConnectToServer = function () { };
    // definition call back function;
    this.sokcetOnOpen = function (event) {
        console.log('WebSocket on connected, event=' + event);
        // alert('已成功與Socket Server 連結！');
    };

    // definition call back function;
    this.socketOnError = function (event) {
        console.log('WebSocket is error:' + event);
    };

    // definition call back function;
    this.socketOnClose = function (event) {
        console.log('WebSocket is close: ' + event);
        this.connect();
    };

    this.socketOnMessage = function (message) {
        console.log('receive Message from Server: ' + message);
    };

    // 定義用戶物件
    this.user = {
        className: 'user',
        token: null,
    };
    this.user.fruitSlots = this;
    this.user.isAuth = this.userAuthCompletes;
    this.user.isAuthError = this.userAuthError;

    this.connect = function () {
        var socketClient = this;

        socketClient.webSocket = new WebSocket(socketClient.webSocketUrl); // 定義並啟動WebSocket連結;
        socketClient.webSocket.socketClient = socketClient; // 增加webSocket一個新物件並指定FruitSlots本身;

        /** webSocket open process; */
        socketClient.webSocket.onopen = function (event) {
            console.log('EWS Frontend: socketClient.webSocket.onopen');

            var socketClient = this.socketClient;
            socketClient.isConnected = true;
            socketClient.isConnectToServer();
            socketClient.sokcetOnOpen(event);

        };

        /** webSocket error process */
        socketClient.webSocket.onerror = function (event) {

            var socketClient = this.socketClient;
            socketClient.socketOnError(event);

        };

        /** webSocket on close Process; */
        socketClient.webSocket.onclose = function (event) {

            var socketClient = this.socketClient;
            socketClient.isConnected = false;
            socketClient.socketOnClose(event);

        };

        /** webSocket on receive message process; */
        socketClient.webSocket.onmessage = function (message) {

            var socketClient = this.socketClient;
            socketClient.socketOnMessage(message);

            var returnValue = message.data;

            payload = JSON.parse(returnValue);

            if (typeof(payload) == 'object') {
                /*
                var command = payload.command;
                var data = payload.data;
                var status = data.status;
                var errorCode = data.errorCode;
                var errorMessage = data.errorMessage;
                var value = data.data;

                // parse command;
                socketClient.internalParse(payload, command, status, errorCode, errorMessage, value);
                */

                socketClient.processMessage(payload);
            } else {
                console.log('onmessage payload type is ' + typeof(payload));
            }
        };
    }

    /** 發送資料給主機 */
    this.sendData = function (message) {
            
        var socketClient = this;
        if (socketClient.isConnected == true) {
            
            // connection is ready
            socketClient.webSocket.send(message);

        }
    }

    /** 發送命令給主機 */
    this.sendCommand = function (sendCommand, sendData) {

        var socketClient = this;
        var data = { };
        data.CMD = sendCommand;
        data.data = sendData;

        if (socketClient.isConnected == true) {
            // connection is ready
            socketClient.webSocket.send(JSON.stringify(data));
        }
    }

    this.setLoginToken = function (token) {
        var socketClient = this;
        socketClient.user.token = token;
    }

    this.userTokenLogin = function () {
        var socketClient = this;
        data = {
            "token":socketClient.user.token,
        }
        console.log('logindata', data);

        socketClient.sendCommand('LoginTokenRequest', data);
    }

    // 定義命令回傳的外部動作;
    this.commandConnectedCallBack = function (status, errorCode, errorMessage, value) { };      // WebSocket連線完成;
    this.commandLoginResultCallBack = function (status, errorCode, errorMessage, value) { };    // 登入完成
    this.commandUserInfoCallBack = function (status, errorCode, errorMessage, value) { };          // 用戶資訊

    this.internalParse = function (payload, command, status, errorCode, errorMessage, value) {
        if (status != 0) {
            console.log('回傳錯誤，錯誤值:' + errorCode + ';訊息:' + errorMessage);
        }

        var socketClient = this;
        if (command == 'connected') {
            if (status == 0 && value != null) {
                socketClient.clientId = value.clientId;
                socketClient.serverStatus = true;
            } else {
                socketClient.serverStatus = false;
            }

            socketClient.commandConnectedCallBack(status, errorCode, errorMessage, value);
        } else if (command == 'LoginResponse') {
            if (status == 0) {
                // 登入成功
                if (socketClient.isLogin == false) {
                    // 重新登入作業
                }

                socketClient.isLogin = true;
                socketClient.user.isAuth();
            } else {
                socketClient.isLogin = false;
                socketClient.user.isAuthError();
            }

            socketClient.commandLoginResultCallBack(status, errorCode, errorMessage, value);    // 執行外部的命令
        }
        else {
            console.log('unknow command, command:' + command);
        }
    }
}