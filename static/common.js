// 넘어온 값이 빈 값인지 체크
// [], {}도 빈 값으로 처리
let isEmpty = function(value){
    if(value == "" || value == null || value == undefined
    || (value != null && typeof value == "object" && !Object.key(value).length)){
        return true;
    }else{
        return false;
    }
};