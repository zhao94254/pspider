package main

import (
	"net/http"
	"fmt"
	"io/ioutil"
	"encoding/json"
	"strconv"
)

func Pindao()  {
	var dat map[string]interface{}
	resp, _ := http.Get("http://open.douyucdn.cn/api/RoomApi/game")
	b, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(b, &dat)
	mapTmp := dat["data"].([]interface{})
	for _, j :=  range mapTmp{
		l := j.(map[string]interface{})
		fmt.Println(l["game_name"], l["cate_id"]) // 获得频道id
		Liveid(l["cate_id"].(float64))
	}
}

func Liveid(pindao float64)  {
	p := strconv.FormatFloat(pindao,'f',0,64)
	resp, _ := http.Get(fmt.Sprintf("http://api.douyu.com/api/v1/live/%s", p))
	// todo parse roomid
	b, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(b))
}


func main()  {
	Pindao()
}

