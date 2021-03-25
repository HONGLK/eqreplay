/** 站台設定OOP版 */
var __Config = {
    Setting :{},
    PageMap : {},
    Init : function(){
        $.getJSON({ url: '/Js/System.json', async: false, dataType: 'json', success: function (data) { __Config.Setting = data;}});
        $.getJSON({ url: '/Js/RouteMap.json', async: false, dataType: 'json', success: function (data) { __Config.PageMap = data; } });
    },
    chkStatus : function(){
        return getCookie(this.Setting.AuthCookie) == '' ? false : true;
    },
    getStatus : function(){
        if(!this.chkStatus())
            return null;
        return JSON.parse(decodeURIComponent(getCookie(this.Setting.AuthCookie)));
    },
    getDefaultPage : function(page){
        return this.PageMap[page] === undefined ? "status_news.htm" : this.PageMap[page];
    }
}
__Config.Init()
/**=============== */

/** 站台設定簡易版 */
/*var _config;
$.getJSON({ url: '/js/System.json', async: false, dataType: 'json', success: function (data) { _config = data; } });
*/
var chkStatus = function () {
    return __Config.chkStatus();
};

var getStatus = function () {
    return __Config.getStatus();
};
/**=============== */

var $fpage = 'status_news.htm',
    $token, $name,
    emailfilter = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/,
    nonumberfilter = /^(\+)?[0-9]{8,}(#[0-9]*)?$/,
    ipfilter = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])((:[0-9]+)?)$/,
    webfilter = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/,
    numberfilter = /^\d+\.?\d*$/,
    Sppattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]"),
    Datefilter = /^([0-9]{3,4})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12][0-9]|3[01])$/,
    wsCallback = function (res) {
        //console.log(res);
    }, mainProcess, CenterMarker, TimeEqRequest = null,TimeEqRequest2 = null, cwbMarker = [], ApiclientAccount = '',wsFunction = function(){},wsFunction2 = function(){},Authorize,WsFlag = 0,auth_functionId = '';

Date.prototype.Format = function (fmt) { //author: meizz 
    if(this == 'Invalid Date' || this == ''){
        return '';
    }else{
        var o = {
            "M+": this.getMonth() + 1, //月份 
            "d+": this.getDate(), //日 
            "h+": this.getHours(), //小时 
            "m+": this.getMinutes(), //分 
            "s+": this.getSeconds(), //秒 
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
            "S": this.getMilliseconds() //毫秒 
        };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }
    
};
Date.prototype.addDays = function (days) {
    //console.log(this);
    this.setDate(this.getDate() + days);
    return this;
};

$(function () {
    //主要執行js
    $('a.searchbtn').click(function (event) {
        event.preventDefault();
        $('header + .title').toggleClass('open');
    });

    //    計算表格高度符合全螢幕
    $(window).on('resize.tableH', function () {
        if ($(window).height() > 760) {
            var HH = $(window).height() - 180;
        } else {
            var HH = $(window).height() - 150;
        }
        $('.mainContent .block.hauto').css('height', (HH - $('.mainContent .block.hlock').height() - 30));
        //        console.log('.mainContent .block.hlock H:'+$('.mainContent .block.hlock').height());
    }).trigger('resize.tableH');
    
    $(window).bind("pageshow", function(event) {
        if (event.originalEvent.persisted) {
            window.location.reload();
        }
    });
});

// fullscreen function
function openFullscreen() {
    var elem = document.documentElement;

    $('header .fullscreen').hide();
    $('header .normalscreen').show();

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) {
        /* Firefox */
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
        /* Chrome, Safari & Opera */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        /* IE/Edge */
        elem.msRequestFullscreen();
    }
}
function closeFullscreen() {
    $('header .normalscreen').hide();
    $('header .fullscreen').show();

    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    }
}
//登出
function actionLogout(Msg) {
    if (__Config.chkStatus()) {
        var token = __Config.getStatus().token;
        var obj = {
            "CMD": "LOGOUT",
            "token": token
        };
        GetDetail(
            '/POSWEB/?action=LOGOUT',
            obj,
            function (res) {
                alert('登出成功');
                setCookie(__Config.Setting.AuthCookie, '', -1);
            },
            function () {
                setCookie('RP', 0, -1);
                //window.location.href = 'default.htm';
            })
    } else {
        alert(Msg);
        //window.location.href = 'default.htm';
    }
}
function actionMember() {
    if (!__Config.chkStatus()) {
        console.log('nice to meet you')
        //actionLogout('登入超時，麻煩請重新登入！');
    } else if (!$('.bodybox').hasClass('accountEdit') && getCookie('RP') == 1) {
        alert('請重新更改密碼！');
        window.location.href = 'account_edit.htm';
    } else {
        if (actionChkTK()) {
            var status = __Config.getStatus();
            $token = status.token;
            $name = status.user_name;
            $('.before-micons.member span').html($name);
            $('header .mainIcon,header .home').attr('href', __Config.getDefaultPage(status.default_page));
            actionWsAlert();
        } else {
            setCookie(__Config.Setting.AuthCookie, '', -1);
            //window.location.href = 'default.htm';
        }
    }
}
function previewFile($target, $file) {
    var preview = $target.get(0);
    var file = $file.get(0).files[0];
    var reader = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}
function actionForget(mail) {
    GetDetail(
        '/POSWEB/?action=FORGETPASSWORD',
        { "CMD": "FORGETPASSWORD", "email": mail, "dev": "dev" },
        function (res) {
            if (res.state == 1) {
                alert(res.errorMessage);
            } else {
                alert('已寄出更改密碼信，請至您的信箱中查看');
                console.log(res.data);
            }
        },
        function () { });
}
function actionChkTK() {
    var bool = false;
    if (!__Config.chkStatus()) {
        return false;
    } else {
        GetDetail(
            '/POSWEB/?action=CHECKTOKEN',
            { "CMD": "CHECKTOKEN", "token": __Config.getStatus().token },
            function (res) {
                if (res.status == 1) {
                    bool = false;
                    alert(res.errorMessage);
                } else {
                    bool = true;
                }
            },
            function () { },false,'');
    }
    return bool;
}
var totalPage = 0,maxPage = 50,nowPage = 1,pagerRe = true,spDetail = false;
function pageInit(callback){
    pager();
    $('.pageblock').find('a.first').click(function(event){
        event.preventDefault();
        nowPage = 1;
        callback()
    })
    $('.pageblock').find('a.last').click(function(event){
        event.preventDefault();
        nowPage = totalPage;
        callback()
    })
    $('.pageblock').find('a.prev').click(function(event){
        event.preventDefault();
        var p_bool = nowPage*1 - 1 > 0 ? true :  false;
        if(p_bool){
            nowPage = nowPage*1 - 1;
            callback()
        }else{
            alert('沒有上一頁');
        }
    })
    $('.pageblock').find('a.next').click(function(event){
        event.preventDefault();
        var p_bool = nowPage*1 + 1 <= totalPage ? true :  false;
        if(p_bool){
            nowPage = nowPage*1 + 1;
            callback()
        }else{
            alert('沒有下一頁');
        }
    })
    $('.pageblock').find('select.pagecount').val(maxPage)
    $('.pageblock').find('select.page').change(function(){
        nowPage = $(this).val()*1;
        $('.pageblock').find('select.page').val(nowPage);
        callback()
    })
    $('.pageblock').find('select.pagecount').change(function(){
        maxPage = $(this).val();
        nowPage = 1;
        $('.pageblock').find('select.page').val(1);
        pagerRe = true;
        $('.pageblock').find('select.pagecount').val($(this).val());
        callback()
    })
}
function pager(){
    $('.pageblock').each(function(i){
        $(this).find('select.page').children().remove();
        for(var x = 0;x < totalPage;x++){
            var p = x + 1;
            $(this).find('select.page').append('<option value="'+p+'">'+p+'</option>')
        }
    })
}

function GetDetail(link, obj, callback, complete, sync, loading) {
    sync = sync || true;
    loading = loading || '';
    var url = __Config.Setting.ServiceAPI + link;
    $.ajax({
        async: !sync,
        crossDomain: true,
        url: url,
        method: "POST",
        data: obj,
        cache:false,
        beforeSend: function () {
            if(typeof loading === 'object')
            {
                //console.log('Loading Show');
                loading.addClass('loading');
            }
            //console.log('beforeSend :' + new Date());
            console.log('object :' + JSON.stringify(obj));
        },
        success: function (response) {
            callback(response);
        },
        complete: function () {
            complete();
            if(typeof loading === 'object')
            {
                //console.log('Loading Hidn');
                loading.removeClass('loading');
            }
        },
        error: function (ex) {
            //console.log('error');
            console.log(ex);
        },
    });
}
/**websocket */
function actionWsAlert() {
    mainProcess = new FrontendClient(__Config.Setting.ServiceWSS);
    mainProcess.userAuthCompletes = function () {
        console.log('ws 登入成功');
        // 登入成功
    };
    mainProcess.userAuthError = function () {
        alert('ws 登入失敗');
        // 登入失敗
    };
    mainProcess.isConnectToServer = function () {
        // 連線上WebSocket Server
        var socketClient = this;
        if (socketClient.user.token != null && socketClient.user.token != '') {
            socketClient.userTokenLogin();
        }
    };
    mainProcess.commandConnectedCallBack = function (status, errorCode, errorMessage, value) {
        if (status == 0) {
            console.log('Frontend WebSocket Server 連線成功');
        } else {
            alert(errorMessage);
        }
    };
    mainProcess.processMessage = function (payload) {
        console.log(payload);
        switch (payload.command) {
            case 'eventAlert':
                GeteventAlert(payload);
                break;
            case 'eqEventResponse':
                console.log('get eqEventResponse');
                AddstatusnewsReport(payload);
                break;
            case 'NewWeatherBureauReport':
                addCwbReport();
                break;
            case 'APIClientUpdated':
                getAPiClient();
                break;
            case 'closeCleintResponse':
                console.log(payload);
                break;
            case 'HeartBeat':
                $('i.system.link').removeClass('off').addClass('on');
                break;
            case 'DataSiteUpdated':
                if(WsFlag == 2){
                    WsFlag = 0;
                    wsFunction();
                }
                break;
            case "MQTTListUpdated":
                GetMQTT();
                break;
            case "EventForwardListUpdated":
                GetEventForward();
                break;
            case "LoginResponse":
                if(payload.status == 0){
                    $('i.system.link').removeClass('off').addClass('on');
                }else{
                    $('i.system.link').removeClass('on').addClass('off');
                }
                break;
        }
    };

    mainProcess.socketOnMessage = function (message) {
        console.log('receive Message from Server: ' + message);
    };
    mainProcess.socketOnClose = function (event) {
        console.log('WebSocket is close: ' + event);
        $('i.system.link').removeClass('on').addClass('off');
        mainProcess.connect();
    };
    mainProcess.setLoginToken(__Config.getStatus().token);
    mainProcess.connect();
}
var setHappend = true, opsw = 0;

function GeteventAlert(payload) {
    var userAlert = __Config.getStatus().alert_level;
    var Eslevl = payload.data.eventId + '_' + payload.data.eventMaxEsLevel;
    var notifyclose = getCookie('notifyClose');
    var notifyclosebtn = getCookie('notifyClosebtn');
    var changeBool = notifyclose.split('_')[0] != payload.data.eventId ? true : notifyclose.split('_')[1] < payload.data.eventMaxEsLevel ? true : false;
    setHappend = payload.data.isEventHappending;
    var statusNewsTime = payload.data.eventStartTime != '' ? new Date(payload.data.eventStartTime).Format("yyyy/MM/dd hh:mm:ss") : '';
    if (changeBool || notifyclosebtn != 1) {
        if (!changeBool && $('.tool.alert').find('.notifybox').length == 0) {
            if (userAlert <= payload.data.eventMaxEsLevel) {
                addAlert(payload.data);
                setCookie('notifyClose', Eslevl, 1);
                $('iframe').remove();
                addAudio('/audio/alert.mp3?' + new Date().getTime());
                $('.alert_bell').addClass('alert');
            }
            $('.time.mobile,.time.pc').html(statusNewsTime);
        } else if (changeBool) {
            /*if (notifyclose.split('_')[1] < payload.data.eventMaxEsLevel && $('body.client').length > 0) {
                mainProcess.sendCommand('receivedEventAlert', payload.data);
            }*/
            if (userAlert <= payload.data.eventMaxEsLevel) {
                setCookie('notifyClosebtn', '', -1);
                if ($('.tool.alert').find('.notifybox').length > 0) {
                    var $notify = $('.tool.alert').find('.notifybox');
                    if ($notify.attr('data-id') != Eslevl) {
                        $notify.hide();
                        addAlert(payload.data);
                        setCookie('notifyClose', Eslevl, 1);
                    }
                } else {
                    addAlert(payload.data);
                    setCookie('notifyClose', Eslevl, 1);
                }
                $('.alert_bell').addClass('alert');
                $('iframe').remove();
                addAudio('/audio/alert.mp3?' + new Date().getTime());
            }
            $('.time.mobile,.time.pc').html(statusNewsTime);
        }
    }
    $('body.client').find('.quakeAlert b.sim').html(payload.data.eventMaxEsLevel);
    $('body.client').find('.quakeAlert b.act').html(payload.data.eventMaxActLevel);
    $('.quakeAlert').removeClass('sim exc').addClass('open').show();
    if(payload.data.eventType == 'Exercise'){
        $('.quakeAlert').addClass('exc');
    }else if(payload.data.eventType == 'Test'){
        $('.quakeAlert').addClass('sim');
    }
    if ($('body.status.ncree').length > 0) {
        if (setHappend && opsw == 0) {
            opsw = 1;
            TimeEqRequest = setInterval(function () {
                mainProcess.sendCommand('requestEqEvent', {});
            }, 500)
            /*TimeEqRequest2 = setInterval(function () {
                wsFunction2();
            }, 1000)*/
        } else if (!setHappend && opsw == 1) {
            opsw = 0;
            clearInterval(TimeEqRequest);
            clearInterval(TimeEqRequest2);
        }
    }
    
}

function addAlert(obj) {
    var $ul = $('<ul/>').addClass('notifybox').attr('data-id', obj.eventId + '_' + obj.eventMaxEsLevel);
    $ul.append('<li>最新地震訊息 <a class="before-micons close"></a></li>');
    $ul.append('<li>' + obj.eventStartTime + '</li>');
    $ul.append('<li>預估震度：' + levelSwitchWord2(obj.eventMaxEsLevel) + '</li>');
    //    $ul.append('<li>預估震央：'+obj.eventMaxActLevel+'</li>');
    $('.tool.alert').append($ul);
    $ul.find('a.close').click(function (event) {
        setCookie('notifyClosebtn', 1, 1);
        $ul.animate({ 'top': '-200px', 'opacity': 0 }, 1000);
        $('.alert_bell').removeClass('alert');
    });
    console.log('send receivedEventAlert');
    mainProcess.sendCommand('receivedEventAlert', obj);
}

function AddstatusnewsReport(payload) {
    if (payload.status == 0) {
        //console.log(SubMarker)
        $.each(SubMarker,function(i,v){
            var markerImg = new TGOS.TGImage(ImgUrl, new TGOS.TGSize(38, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(10, 33));
            v.setIcon(markerImg);
        })
        $('body.status.ncree .cwb .tablebox.sn01').find('ul.item').remove();
        $('body.status.ncree .cwb .count').html(payload.data.length);
        $.each(payload.data, function (i, v) {
            var $ul = $('<ul/>').addClass('item').attr('id', v.DeviceId);
            $ul.append('<li>' + v.DeviceName + '</li>');
            $ul.append('<li>' + levelSwitchWord2(v.EsLevel) + '</li>');
            $ul.append('<li>' + v.PublishTime + '</li>');
            $ul.append('<li>' + levelSwitchWord2(v.ActLevel) + '</li>');
            var now = new Date();
            var pub = new Date(v.PublishTime);
            var disTime = Math.round(parseInt(now - pub) / 1000);
            $ul.append('<li>' + disTime + '</li>');
            $('body.status.ncree .cwb .tablebox.sn01').append($ul);
            var marker = SubMarker[v.DeviceId];
            //console.log(marker);
            if(typeof marker === 'object'){
                var imagelevel = levelSwitch(v.EsLevel);
                var markerImg = new TGOS.TGImage('/Images/map/lo' + imagelevel + '.png', new TGOS.TGSize(38, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(10, 33));
                marker.setIcon(markerImg);
                $ul.click(function(){
                    setMapCenter(pMap,marker.getPosition());
                })
            }
        });
    }
}
function getAPiClient() {
    GetDetail(
        '/POSWEB/?action=APICLIENTSTATUSLIST',
        { "CMD": "APICLIENTSTATUSLIST", "token": __Config.getStatus().token, "active_status": "active" },
        function (res) {
            var data = res.data;
            if (res.status == 0) {
                var c = 0;
                $('body.status.device .tablebox.st04').find('ul.item').remove();
                $.each(res.data, function (i, v) {
                    if (v.Remark_Status == '連線') {
                        addAPIClient(v);
                        c++;
                    }
                });
                $('.tabletab.t04 b.count').html(c + '/' + res.total);
            } else {
                console.log(res);
            }
        },
        function () {
            $('body.status.device #alertbox .submit').off('click');
            $('body.status.device #alertbox .submit').click(function (event) {
                event.preventDefault();
                if($('#reason').val() == ''){
                    $('body.status.device #alertbox h6.alert').show();
                }else{
                    mainProcess.sendCommand('closeClient', { "uid": ApiclientAccount, "reason": $('#reason').val() });
                    $.fancybox.close();
                }
            });
        });
}

function addAPIClient(obj) {
    if($('body.status.device .tablebox.st04').length > 0){
        var $ul = $('<ul/>').addClass('item').attr('id', obj.User_ID);
        $ul.append('<li>' + obj.User_ID + '</li>');
        $ul.append('<li>' + obj.Company + '</li>');
        $ul.append('<li>' + obj.User_Name + '</li>');
        $ul.append('<li>' + obj.Phone + '</li>');
        $ul.append('<li><a class="before-micons online fancybox" href="#alertbox"></a></li>');
        $('body.status.device .tablebox.st04').append($ul);
        $ul.find('a.fancybox').fancybox({
            beforeShow: function () {
                ApiclientAccount = obj.User_ID;
                $('#alertbox .account').html(obj.User_ID);
            }
        });
    }
}

function addCwbReport() {
    GetDetail(
        '/POSWEB/?action=GETLATESTEQREPORT',
        { "CMD": "GETLATESTEQREPORT", "token": __Config.getStatus().token },
        function (res) {
            var data = res.report;
            if (res.status == 0) {
                $('.cwbreport #MSG').html(data.identifier);
                $('.cwbreport #MSG_time').html(data.originTime);
                $('.cwbreport #MSG_Level').html(data.magnitudeValue);
                $('.cwbreport #MSG_deep').html(data.depth);
                $('.cwbreport #MGS_center').html(data.location);
                $('.cwbreport #MGS_latlon').html(data.epicenterLon + '°E ' + data.epicenterLat + '°N');
                $('b.time.mobile,b.time.pc').html(new Date(data.originTime).Format("yyyy/MM/dd hh:mm:ss"));
                var Center = '/Images/map/center.png';
                var markerPosition = WGS84toTWD97(data.epicenterLon, data.epicenterLat);
                var markerImg = new TGOS.TGImage(Center, new TGOS.TGSize(38, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(10, 33));
                if (typeof CenterMarker == 'object') CenterMarker.setVisible(false);
                CenterMarker = CreateMarker(pMap, markerPosition, '', markerImg);
                CenterMarker.setZIndex(5);
                $('.cwbreport a.small').click(function () {
                    setMapCenter(pMap, markerPosition);
                });

                $('.hauto .tablebox.sn04').find('ul.item').remove();
                if (cwbMarker.length > 0) {
                    $.each(cwbMarker, function (j, x) {
                        x.setVisible(false);
                    });
                }
                $('.hauto .count').html(data.REPORT.length);
                $.each(data.REPORT, function (i, v) {
                    if (data.REPORT.length > 0 && $('.hauto .tablebox.sn04').length > 0) {
                        var $c_ul = $('<ul/>').addClass('item');
                        $c_ul.append('<li>' + v.Name + '</li>')
                        $c_ul.append('<li>' + levelSwitchWord2(v.PGA_Level) + '</li>');
                        $('.hauto .tablebox.sn04').append($c_ul);
                    }
                    var level = levelSwitch(v.PGA_Level);
                    var PGAimage = '/Images/map/l' + level + '.png';
                    var c_markerPosition = WGS84toTWD97(v.Longitude, v.Latitude);
                    var c_markerImg = new TGOS.TGImage(PGAimage, new TGOS.TGSize(38, 33), new TGOS.TGPoint(0, 0), new TGOS.TGPoint(10, 33));
                    var marker = CreateMarker(pMap, c_markerPosition, '', c_markerImg);
                    marker.setZIndex(1);
                    cwbMarker.push(marker);
                });
            }
        },
        function () {
        }
    );
}

function showAlert(payload) {
    var eventDate = new Date(payload.data.eventStartTime).addDays(1);
    if (beforetime(eventDate)) {
        $('a.allon').click(function (event) {
            event.preventDefault();
            if ($('.quakeAlert').hasClass('open')) {
                $('.quakeAlert').removeClass('open').hide();
            } else {
                $('.quakeAlert').addClass('open').show();
            }
        });
    } else {
        $('.quakeAlert').removeClass('open').hide();
    }
}
/**============= */
//1
function defaultInit() {
    $('.default a.loginforget').click(function (event) {
        event.preventDefault();
        $('.default .bodybox').addClass('forget');
    });
    $('.default .forgetblock a.close').click(function (event) {
        event.preventDefault();
        $('.default .bodybox').removeClass('forget');
    });
    $('.default .forgetblock a.submit').click(function (event) {
        event.preventDefault();
        if ($('.fogetemail').val() == '') {
            alert('請填寫申請帳號的email');
        } else {
            actionForget($('.fogetemail').val());
            $('.default .bodybox').removeClass('forget');
        }
    });

    $('header .fullscreen').click(function () {
        openFullscreen();
    });
    $('header .normalscreen').click(function () {
        closeFullscreen();
    });
    $('input#account,input#password').keydown(function(event){
        if( event.which == 13 ) {
            $('.loginblock .btn.orange').trigger('click');
        }
    });
    $('input.fogetemail').keydown(function(event){
        if( event.which == 13 ) {
            $('.default .forgetblock a.submit').trigger('click');
        }
    });

    //登入
    $('.loginblock .btn.orange').click(function (event) {
        event.preventDefault();
        if ($('#account').val() == '') {
            alert('請輸入帳號！');
        } else if ($('#password').val() == '') {
            alert('請輸入密碼！');
        } else if ($('input#account').val().match(Sppattern)) {
            alert('帳號不能含有特殊字元，請重新填寫');
        } else  {
            var bcrypt = dcodeIO.bcrypt;
            var key = '';
            var obj = {
                "CMD": "Login",
                "uid": $('#account').val(),
                "pwd": ''
            };
            $.ajax({
                async: false,
                crossDomain: true,
                url: __Config.Setting.ServiceAPI + '/POSWEB/?action=GETKEY',
                method: "POST",
                data: { "CMD": "GetKey", "uid": $('#account').val() },
                success: function (response) {
                    if (response.status == 0) {
                        key = response.data;
                        obj.pwd = bcrypt.hashSync(md5($('#password').val()) + key, 10);
                        GetDetail(
                            '/POSWEB/?action=LOGIN',
                            obj,
                            function (res) {
                                if (res.status == 1) {
                                    alert(res.errorMessage);
                                    $('#password').val('');
                                } else {
                                    var data = res.data;
                                    //取得地圖警示設定檔
                                    GetDetail(
                                        '/POSWEB/?action=GETCLIENTMAPSETTING',
                                        { "CMD": "GETCLIENTMAPSETTING", "token": data.token, "client_id": data.uid },
                                        function (res) {
                                            if (res.status == 0) {
                                                var alertData = res.data;
                                                if (alertData.length > 0) {
                                                    data.alert_level = alertData[0].alert_level;
                                                    data.get_alert = alertData[0].get_alert;
                                                    data.get_alert = alertData[0].get_report;
                                                    data.get_test = alertData[0].get_test;
                                                } else {
                                                    data.alert_level = 1;
                                                    data.get_alert = 0;
                                                    data.get_report = 0;
                                                    data.get_test = 0;
                                                }
                                            }else{
                                                data.alert_level = 1;
                                                data.get_alert = 0;
                                                data.get_report = 0;
                                                data.get_test = 0;
                                            }
                                        },
                                        function () {
                                            var Mval = encodeURIComponent(JSON.stringify(data));
                                            setCookie(__Config.Setting.AuthCookie, Mval, 1);
                                            
                                            if(data.need_reset_password == 1){
                                                alert('請建立您的新密碼！');
                                                setCookie('RP', 1, 1);
                                                window.location.href = 'account_edit.htm';
                                            }else{
                                                setCookie('RP', 0, -1);
                                                window.location.href = __Config.getDefaultPage(data.default_page);
                                            }
                                            
                                        },false,'');
                                }
                            },
                            function () {
                                //console.log('Login complete:'+ new Date().Format("yyyy-MM-dd hh:mm:ss"))
                                ////console.log('complete')
                            },false,'');
                    } else {
                        alert(response.errorMessage);
                    }
                },
                complete: function () {
                    //console.log('Getkey complete:'+ new Date().Format("yyyy-MM-dd hh:mm:ss"))
                    //console.log('obj:'+JSON.stringify(obj))
                }
            });
        }
    });
}
//登入
function signupInit() {
    var CityTown = [];
    //取得地區
    GetDetail(
        '/POSWEB/?action=GETCOUNTYDATA',
        { "CMD": "GETCOUNTYDATA" },
        function (res) {
            var data = res.data;
            $('#city').children().remove();
            $('#city').append('<option value="">選擇縣市</option>');
            $.each(data, function (i, v) {
                $('#city').append('<option value="' + v.ID + '">' + v.Name + '</option>');
            });
        },
        function () {
            $('#city').change(function () {
                var value = $(this).val();
                $('#town').children().remove();
                $('#town').append('<option value="">選擇鄉鎮市區</option>');
                if (value != '') {
                    GetDetail(
                        '/POSWEB/?action=GETTOWNDATA',
                        { "CMD": "GETTOWNDATA", "coun_id": value },
                        function (res) {
                            var data = res.data;
                            $.each(data, function (i, v) {
                                var $op = $('<option/>').val(v.ID).html(v.Name);
                                //'<option value="'+v.ID+'">'+v.Name+'</option>';
                                $('#town').append($op);
                                $op.data('lon', v.Lon);
                                $op.data('lon', v.Lat);
                            });
                        },
                        function () {

                        });
                }
            });
        });
    //送出按鈕
    $('.btn.orange').click(function (event) {
        event.preventDefault();
        if ($('#city').val() == '') {
            alert('請選擇縣市');
        } else if ($('#town').val() == '' && $('#town').find('option').length > 1) {
            alert('請選擇鄉鎮市區');
        } else if ($('#addr').val() == '') {
            alert('請填寫地址');
        } else if ($('#account').val() == '') {
            alert('請填寫帳號');
        } else if ($('#password').val() == '') {
            alert('請填寫密碼');
        } else if ($('#chkpassword').val() == '') {
            alert('請填寫確認密碼');
        } else if ($('#name').val() == '') {
            alert('請填寫聯絡人');
        } else if ($('#career').val() == '') {
            alert('請填寫職稱');
        } else if ($('#career').val() == '') {
            alert('請填寫職稱');
        } else if ($('#tel').val() == '') {
            alert('請填寫聯絡電話');
        } else if ($('#tel').val() == '') {
            alert('請填寫聯絡電話');
        } else if ($('#password').val() != '' && $('#password').val().length < 8) {
            alert('密碼需填寫八碼以上');
        } else if ($('#password').val() != $('#chkpassword').val()) {
            alert('確認密碼填寫錯誤');
        } else if ($('#tel').val() != '' && !nonumberfilter.test($('#tel').val())) {
            alert('聯絡電話請填寫數字');
        } else if ($('#email').val() != '' && !emailfilter.test($('#email').val())) {
            alert('EMail請填寫正確的格式');
        } else if (!checkAccount($('#account').val())) {
            alert('此帳號已有人使用');
        } else {
            $('input[id!="email"][id!="tel"]').each(function (i) {
                var value = $(this).val();
                var result = value.match(Sppattern);
                if (result) {
                    alert('該輸入含有特殊字元，請重新填寫');
                    $(this).focus();
                    return false;
                }
            });

            var obj = {
                "CMD": "SIGNUP",
                "ID": $('#account').val(),
                "Pwd": md5($('#password').val()),
                "Name": $('#name').val(),
                "UnitName": "admin",
                "Position": $('#career').val(),
                "Tel": $('#tel').val(),
                "Email": $('#email').val(),
                "County": $('#city').val(),
                "Town": $('#town').val(),
                "Address": $('#addr').val(),
                "Lat": "25.0119",
                "Lng": "121.5179",
                "UnitType": "5",
                "UnitType2": "501",
                "Role": "normal"
            };
            GetDetail(
                '/POSWEB/?action=SIGNUP',
                obj,
                function (res) {
                    var data = res.data;
                    if (res.status == 1) {
                        alert(res.errorMessage);
                    } else {
                        alert('申請成功');
                        window.location.href = 'default.htm';
                    }
                },
                function () {

                });
        }
    });

    $('input[id!="email"][id!="tel"]').change(function () {
        var value = $(this).val();
        var result = value.match(Sppattern);
        if (result) {
            alert('該輸入含有特殊字元，請重新填寫');
            $(this).focus();
        }
    });
}//帳號申請

function isEmpty(obj) {
    if (obj == null) return true;
    if (obj.length > 0) return false;
    if (obj.length === 0) return true;
    if (typeof obj !== "object") return true;
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }
    return true;
}

function checkAccount(account) {
    var chkbool = false;
    GetDetail(
        '/POSWEB/?action=CHECKACCOUNTID',
        { "CMD": "CHECKACCOUNTID", "AccountID": account },
        function (res) {
            var data = res.data;
            if (res.status == 0) {
                chkbool = true;
            } else {
                chkbool = false;
            }
        },
        function () { },false,'')
    return chkbool;
}

function sort(selector, selector_child, index, order) {
    $(selector).children(selector_child).sort(function (a, b) {
        var A = $(a).find('li:eq(' + index + ')').text().toUpperCase();
        var B = $(b).find('li:eq(' + index + ')').text().toUpperCase();
        if (A == '') {
            A = $(a).find('li:eq(' + index + ') b').attr('title') == undefined ? null : $(a).find('li:eq(' + index + ') b').attr('title');
        }
        if (B == '') {
            B = $(b).find('li:eq(' + index + ') b').attr('title') == undefined ? null : $(b).find('li:eq(' + index + ') b').attr('title');
        }

        if (order == 'des') {
            if (A == null) {
                return 1;
            } else if (B == null) {
                return -1;
            } else if (isNaN(A) && isNaN(B)) {
                if (isNaN(Date.parse(A)) && isNaN(Date.parse(B))) {//不是日期
                    return (A < B) ? -1 : (A > B) ? 1 : 0;
                } else {
                    return Date.parse(A) - Date.parse(B);
                }
            } else {
                return A - B;
            }

        } else {
            if (A == null) {
                return 1;
            } else if (B == null) {
                return -1;
            } else if (isNaN(A) && isNaN(B)) {
                if (isNaN(Date.parse(A)) && isNaN(Date.parse(B))) {//不是日期
                    return (A < B) ? 1 : (A > B) ? -1 : 0;
                } else {
                    return Date.parse(B) - Date.parse(A);
                }
            } else {
                return B - A;
            }

        }
    }).appendTo(selector);
}

function TitleSortInit() {
    // 表格標頭升降冪
    $('div.tablebox ul.header > li').click(function () {
        if ($(this).hasClass('focus')) {
            if ($(this).hasClass('des')) {
                $(this).removeClass('des');
                sort('div.tablebox', 'ul.item', $(this).index(), 'asc')
            } else {
                $(this).addClass('des');
                sort('div.tablebox', 'ul.item', $(this).index(), 'des')
            }
        } else {
            $('div.tablebox ul.header > li').removeClass('focus des');
            $(this).addClass('focus')
            sort('div.tablebox', 'ul.item', $(this).index(), 'asc')
        }
    });
}

function addAudio(src) {
    if (($('.R_function a.alert').length > 0 && !$('.R_function a.alert').hasClass('off')) || $('.R_function a.alert').length == 0) {
        var iframe = $('<iframe/>');
        iframe.attr('src', src)
        iframe.attr('type', 'audio/mp3')
        iframe.attr('allow', 'autoplay')
        iframe.css('display', 'none')
        $('body').append(iframe);
    }
}

function isNDate(value) {
    if (new Date(value).toString() == 'Invalid Date') {
        if (value == '') {
            return false;
        } else {
            return true;
        }
    } else {
        return false;
    }
}

function levelSwitch(level) {
    var tmp = 1;
    switch (level.toString()) {
        case '0':
            tmp = 0;
            break;
        case '1':
            tmp = 1;
            break;
        case '2':
            tmp = 2;
            break;
        case '3':
            tmp = 3;
            break;
        case '4':
            tmp = 4;
            break;
        case '5':
            tmp = 5;
            break;
        case '5.5':
            tmp = '5b';
            break;
        case '6':
            tmp = 6;
            break;
        case '6.5':
            tmp = '6b';
            break;
        case '7':
            tmp = 7;
            break;
    }
    return tmp;
}
function levelSwitchWord(level) {
    var tmp = 1;
    switch (level.toString()) {
        case '0':
            tmp = 0;
            break;
        case '1':
            tmp = 1;
            break;
        case '2':
            tmp = 2;
            break;
        case '3':
            tmp = 3;
            break;
        case '4':
            tmp = 4;
            break;
        case '5':
            tmp = '5弱';
            break;
        case '5.5':
            tmp = '5強';
            break;
        case '6':
            tmp = '6弱';
            break;
        case '6.5':
            tmp = '6強';
            break;
        case '7':
            tmp = 7;
            break;
    }
    return tmp;
}
function levelSwitchWord2(level) {
    var tmp = 1;
    switch (level.toString()) {
        case '0':
            tmp = 0;
            break;
        case '1':
            tmp = 1;
            break;
        case '2':
            tmp = 2;
            break;
        case '3':
            tmp = 3;
            break;
        case '4':
            tmp = 4;
            break;
        case '5':
            tmp = '5-';
            break;
        case '5.5':
            tmp = '5+';
            break;
        case '6':
            tmp = '6-';
            break;
        case '6.5':
            tmp = '6+';
            break;
        case '7':
            tmp = 7;
            break;
        default:
            tmp = level;
            break;
    }
    return tmp;
}

function checkAuth(function_id,type){
    //type：R(讀取),C(新增),M(修改),D(刪除)；'R,C,M' -> reutrn [true,true,false];
    var obj = {};
    GetDetail(
            '/POSWEB/?action=CHKAUTHORIZATION',
            {
                "CMD":'CHKAUTHORIZATION',
                "group_iguid":__Config.getStatus().group_id,
                "function_id":function_id,
                "token":__Config.getStatus().token
            },
            function(res){
                if(res.status == 0){
                    var authtype = type.split(',');
                    var auth =  res.data[0].authorize.split(',');
                    var num = -1;
                    $.each(authtype,function(i,v){
                        var type = '';
                        switch (v){
                            case 'R':
                                num = auth.findIndex(function(v){return v === '{讀取}'});
                                break;
                            case 'C':
                                num = auth.findIndex(function(v){return v === '{新增}'});
                                break;
                            case 'M':
                                num = auth.findIndex(function(v){return v === '{修改}'});
                                break;
                            case 'D':
                                num = auth.findIndex(function(v){return v === '{刪除}'});
                                break;
                        }
                        if(num >= 0){
                            obj[v] = true;
                        }else{
                            obj[v] = false;
                        }
                    })
                }
            },
            function(){
                auth_functionId = function_id;
                
            })
    return obj;
}

function AuthMenu(group){
    var $target = $('nav.menu .list');
    GetDetail(
        '/POSWEB/?action=GETMAINMENU',
        {"CMD":"GETMAINMENU","group_id":group},
        function(res){
            if(res.status == 0){
                $.each(res.data,function(i,v){
                    var p_id = '';
                    if(v.parent == -1){
                        p_id = v.id;
                        $target.append('<dl data-parent="'+v.id+'"></dl>');
                        $target.find('dl[data-parent="'+p_id+'"]').append('<dt>'+v.title+'</dt>');
                    }else{
                        p_id = v.parent;
                        if(v.function.length > 0){
                            $target.find('dl[data-parent="'+p_id+'"]').append('<dt>'+v.title+'</dt>');
                        }
                    }
                    
                    $.each(v.function,function(j,w){
                        $target.find('dl[data-parent="'+p_id+'"]').append('<dd><a data-code="'+w.second_func_code+'" href="'+w.second_func_url+'">'+w.second_func_title+'</a></dd>'); 
                    })
                })
            }
        },
        function(){
            $('nav a[data-code="'+auth_functionId+'"]').addClass('focus');
            $('nav a[data-code="'+auth_functionId+'"]').parents('dl').addClass('focus');
            $target.find('dl').each(function(){
                if($(this).find('dd').length == 0){
                    $(this).remove();
                }
            })
        }
    )
}
//mqtt連線&事件原始資料連線
function GetMQTT(){
    $.ajax({
        async: true,
        crossDomain: true,
        url: __Config.Setting.ServiceAPI +'/POSWEB/?action=APIMQTTONLINELIST',
        method: "POST",
        data: {
            "CMD":"APIMQTTONLINELIST",
            "token":getStatus().token,
            "active_status":"active"
        },
        cache:false,
        success: function (response) {
           if(response.status == 0){
                var count = 0;
                $('.tablebox.st08').find('ul.item').remove();
                $.each(response.data,function(i,v){
                    // check if user is online, will add into the list

                    if(v.Remark_Status == '連線') {

                        count++;
                        var $ul = $('<ul/>').addClass('item')
                        $ul.append('<li>'+v.User_ID+'</li>');
                        $ul.append('<li>'+v.Company+'</li>');
                        $ul.append('<li>'+v.User_Name+'</li>');
                        $ul.append('<li>'+v.Phone+'</li>');
                        $ul.append('<li><a class="before-micons online fancybox" href="#alertbox"></a></li>');
                        $('body.status.device .tablebox.st08').append($ul);
                        $ul.find('a.fancybox').fancybox({
                            beforeShow: function () {
                                ApiclientAccount = v.User_ID;
                                $('#alertbox .account').html(v.User_ID);
                            }
                        });

                    }

                })
                $('.tabletab.t08 b.count').html(count + '/' + response.total);
           }
        },
        complete: function () {}
    });
}
function GetEventForward(){
    $.ajax({
        async: true,
        crossDomain: true,
        url: __Config.Setting.ServiceAPI +'/POSWEB/?action=APIEVENTFORWARDLIST',
        method: "POST",
        data: {
            "CMD":"APIEVENTFORWARDLIST",
            "token":getStatus().token,
            "active_status":"active"
        },
        cache:false,
        success: function (response) {
            $('.tablebox.st09').find('ul.item').remove();
           if(response.status == 0){
                var count = 0;
                $.each(response.data,function(i,v){

                    // check if user is online, will add into the list

                    if(v.Remark_Status == '連線') {

                        count++;
                        var $ul = $('<ul/>').addClass('item')
                        $ul.append('<li>'+v.User_ID+'</li>');
                        $ul.append('<li>'+v.Company+'</li>');
                        $ul.append('<li>'+v.User_Name+'</li>');
                        $ul.append('<li>'+v.Phone+'</li>');
                        $ul.append('<li><a class="before-micons online fancybox" href="#alertbox"></a></li>');
                        $('body.status.device .tablebox.st09').append($ul);
                        $ul.find('a.fancybox').fancybox({
                            beforeShow: function () {
                                ApiclientAccount = v.User_ID;
                                $('#alertbox .account').html(v.User_ID);
                            }
                        });

                    }
                    
                })
                $('.tabletab.t09 b.count').html(count + '/' + response.total);
           }
        },
        complete: function () {},
        error: function (ex) {
            console.log(ex);
        }
    });
}