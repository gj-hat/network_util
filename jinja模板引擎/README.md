# 使用说明


###  数据源说明
1. 将模版文件放到`templates`文件夹下
2. 数据源1 在`data`文件夹下 excel格式 
3. 数据源2 是数据库 通过`config.properties`中的`DB_CONFIG`变量配置
4. 修改`config.properties`文件中的`TEMPLATE_FILE`变量为模版文件名
5. 数据源优先级在`config.properties`中的`DATA_SOURCE`变量配置(枚举类型 excel 、 db 、空)

### 模版生成原则
1. `{{xx}}` 双花括号内的是变量名  届时和模板的变量名对应即可
2. `$xx$` 美元符号 中间的为预变量 
3. `$template$` 为模板 优先级最高 如果有则不向下匹配  必须有这个字段列（后期考虑移除强制）
4. `$template_id$` 为模版id  优先级次于template  （后期考虑移除强制）
5. 如果以上均为空 则使用本地默认的模板`template/DemoTemplate.template`内。
6. `&xx&`为输出标记 默认为&res&  如果有其他的 可以自定义   这个还没开发后期会补上
  
