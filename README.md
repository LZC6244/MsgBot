# DingTalkBot
群机器人是钉钉群的高级扩展功能。群机器人可以将第三方服务的信息聚合到群聊中，实现自动化的信息同步。

- 开发环境： `python 3.7.5`
- 使用需求：起码拥有一个钉钉群聊天机器人（[如何申请](#dingtalk)）

## 消息类型及DEMO
- text 类型  
  ![]()

- link 类型  
  ![]()
  
- markdown 类型  
  ![]()
  
  **ps:** 目前只支持md语法的子集，具体支持的元素如下（钉钉限定）
    
  ```text
  标题
  # 一级标题
  ## 二级标题
  ### 三级标题
  #### 四级标题
  ##### 五级标题
  ###### 六级标题
  
  引用
  > A man who stands for nothing will fall for anything.
  
  文字加粗、斜体
  **bold**
  *italic*
  
  链接
  [this is a link](http://name.com)
  
  图片
  ![](http://name.com/pic.jpg)
  
  无序列表
  - item1
  - item2
  
  有序列表
  1. item1
  2. item2
  ```  

- 整体跳转 ActionCard 类型  
  ![]()
  
- 独立跳转 ActionCard 类型  
  ![]()
  
- FeedCard 类型  
  ![]()

# 参考链接

- <span id="dingtalk">[钉钉开发文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)</span>