var ImgLink = 'https://api.tgos.tw/TGOS_API/images/marker2.png',eqCenterImg = '';

function MapInit(id){
    var pOMap = document.getElementById(id);  //宣告一個網頁容器
    var MapOption = {
        scaleControl:true,
        navigationControl: true,
        navigationControlOptions: {
            controlPosition: TGOS.TGControlPosition.LEFT_CENTER,
            navigationControlStyle: TGOS.TGNavigationControlStyle.SMALL
        }
    }
    var pMap = new TGOS.TGOnlineMap(pOMap, TGOS.TGCoordSys.EPSG3826,MapOption);
    
    pMap.setZoom(3);
    pMap.setCenter(new TGOS.TGPoint(370000, 2620000));

    return pMap;
}
function CreateMarker(map,position,title,img){
    return new TGOS.TGMarker(map, position, title, img);
}
function setMapCenter(map,position){
    map.setCenter(position); 
    map.setZoom(7);
}
//回傳值是 TGPoint
function WGS84toTWD97(x,y){
    var X84 = Number(x);
    var Y84 = Number(y);
    var TT = new TGOS.TGTransformation();
    TT.wgs84totwd97(X84,Y84);
    return new TGOS.TGPoint(TT.transResult.x ,TT.transResult.y);
}
var fill = null;
function locateDistrict(map,districtInput) {  //加入行政區定位
    if (fill) {fill.setMap(null)};
    var locator = new TGOS.TGLocateService()
    locator.locateTWD97({
        district: districtInput
    }, function (e, status) {
        if (status != TGOS.TGLocatorStatus.OK) {
            alert('查無行政區');
            return;
        }
        /*marker.setVisible(true);  //設定標記點標示行政區中心
        marker.setPosition(e[0].geometry.location);*/
        map.fitBounds(e[0].geometry.viewport);  
        map.setZoom(map.getZoom() - 1);
        //調整畫面符合行政區邊界
        var pgn = e[0].geometry.geometry;
        console.log(pgn);
        //讀取行政區空間資訊
        fill = new TGOS.TGFill(map, pgn, {
        //將行政區空間資訊以面圖徵呈現
            fillColor: '#00AAAA',
            fillOpacity: 0.2,
            strokeColor: '#009090',
            strokeWeight: 5,
            strokeOpacity: 1
        });
    });
}