package base

import (
	"net/http"
	"fmt"
	"io/ioutil"
	"encoding/json"
	"strconv"
)

// 遇到的一点问题。。没有找到类似于python 中的extend函数
// 直接通过指针来传递一个数组，直接通过指针来改变。


const maxOnline  = 500000

func Pindao() []string {
	var dat map[string]interface{}
	var res []string
	p := &res
	resp, _ := http.Get("http://open.douyucdn.cn/api/RoomApi/game")
	b, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(b, &dat)
	mapTmp := dat["data"].([]interface{})
	for _, j :=  range mapTmp{
		l := j.(map[string]interface{})
		fmt.Println("频道名：", l["game_name"], l["cate_id"]) // 获得频道id
		Liveid(l["cate_id"].(float64), p)
		fmt.Println(len(*p))
	}
	fmt.Println("result..", *p)
	return *p
}

func Liveid(pindao float64, point *[]string)  {
	p := strconv.FormatFloat(pindao,'f',0,64)
	resp, _ := http.Get(fmt.Sprintf("http://api.douyu.com/api/v1/live/%s", p))
	var dat map[string]interface{}
	b, _ := ioutil.ReadAll(resp.Body)
	json.Unmarshal(b, &dat)
	mapTmp := dat["data"].([]interface{})
	for _, j := range mapTmp{
		l := j.(map[string]interface{})
		if l["online"].(float64) > maxOnline{
			*point = append(*point, l["room_id"].(string))
		}
	}
}

