QQ_pic_bak
==========

QQ本身提供了备份聊天记录文字信息并还原的功能，但却不支持备份图片并还原，如果不定期清理图片，文件夹会越来越大，清理图片，有些不想删除的图片又没了，故该工具产生，可备份特定对象聊天记录中的图片，跟QQ本身聊天记录备份相结合，可完美备份特定对象的聊天记录。

## Requirements ##

* [Python 2.7](https://www.python.org/downloads/) (recommend)
* Windows

## How to use ##
备份方法<br />
1. 利用qq的聊天记录导出工具，将要备份的聊天记录导出为mht格式<br />
2. 将该工具跟mht文件放于同一文件夹下<br />
3. 打开该工具<br />
4. 输入QQ号<br />
5. 工具会在当前文件夹下生成bak文件夹，里面存放需要保存的图片及文件夹结构< />

恢复方法<br />
1. 找到QQ存放聊天记录的文件夹，一般在“我的文档”<br />
2. 复制备份的文件夹至相应的目录<br />
3. 重启QQ<br />