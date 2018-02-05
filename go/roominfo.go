package main

import (
	"net/http"
	"fmt"
	"io/ioutil"
	"encoding/json"
)

func main()  {
	var dat map[string]interface{}
	resp, _ := http.Get("http://open.douyucdn.cn/api/RoomApi/game")
	b, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(b, &dat)
	//fmt.Println(dat["data"]) // 获取频道
	for _, j :=  range dat{
		fmt.Println(j)
		fmt.Println("\n")
	}

}

