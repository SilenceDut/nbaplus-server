# nbaplus-server
Server of The NBAPlus APP 。
这是NBAPlus 的Web后台服务器部分，用python语言实现，部署在新浪SAE平台。
由于是初学python并且是第一次搭建后台，所以可能有很多不规范的地方,这里主要是提供一种自己做APP时搭建服务器部分的思路。
希望能帮到有这部分需要但不知如何入手的人，更希望对着比较了解的人能提供一些建议。
程序采用的Web框架是Flask,开启一些定时任务来爬取一些站点的信息并进行存储，通过restful api 为APP提供接口。
由于访问的站点未经授权，所以关于第三方api站点部分的文件未上传，但不影响对整体的了解，如果你有需要可以email（silencedutchman@foxmail.com）我，我会把那部分文件发你，切忌勿用于商业应用，只限学习交流。
