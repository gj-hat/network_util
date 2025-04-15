## 小米网络刷配置V2脚本使用说明

### 依赖管理
> 使用py文件时需要安装
```shell
pip3 install netmiko
```



### 更新日志
1. 优化底层代码，新增异常处理，日志处理，设备回显等增强可用性
2. 使用`properties`文件管理配置
3. `ssh`工具修改为`netmiko`，支持更多设备，解决长命令回显问题
4. 优化结果回显


### 使用说明
本脚本是基于excel表格内容刷入配置
#### 核心参数
1. 需要几个核心参数 就实际使用而言 ip和cmd是必要在表格中出现的 其他参数使用默认也可以
   1. device_type 设备类型  优先从表格拿数据 如果表格没有则在配置文件的`device_type`中拿取。 表格实际的字段名可以在配置中间中`excel_device_type`配置
   2. excel_username 用户名  优先从表格拿数据 如果表格没有则在配置文件的`username`中拿取。 表格实际的字段名可以在配置中间中`excel_username`配置
   3. excel_password 密码  优先从表格拿数据 如果表格没有则在配置文件的`password`中拿取。 表格实际的字段名可以在配置中间中`excel_password`配置
   4. excel_port 端口号  优先从表格拿数据 如果表格没有则在配置文件的`port`中拿取。 表格实际的字段名可以在配置中间中`excel_port`配置
   5. excel_identity 身份(提供两种类型user/root)  优先从表格拿数据 如果表格没有则在配置文件的`identity`中拿取。 表格实际的字段名可以在配置中间中`excel_identity`配置
   6. excel_is_save 是否保存配置(最好不要使用命令保存)  优先从表格拿数据 如果表格没有则在配置文件的`is_save`中拿取。 表格实际的字段名可以在配置中间中`excel_is_save`配置
   7. excel_enable_password enable密码（多用于思科锐捷等需要enable的设备）  优先从表格拿数据 如果表格没有则在配置文件的`enable_password`中拿取。 表格实际的字段名可以在配置中间中`excel_enable_password`配置
   8. excel_ip 设备ip  优先从表格拿数据 如果表格没有则在配置文件的`ip`中拿取。 表格实际的字段名可以在配置中间中`excel_ip`配置
   9. excel_cmd 执行的命令  优先从表格拿数据 如果表格没有则在配置文件的`cmd`中拿取。 表格实际的字段名可以在配置中间中`excel_cmd`配置

#### 额外功能说明

可以在这里对输出结果进行增强 例如抓取设备配置时候 可以对结果进行格式化并放置在某列中
``` python
# 这是增强方法 如果需要对返回结果进行处理 可以在这里进行处理 否则可以直接返回结果
def enhancement_method(in_var):
    data_excel.write_excel_cell(sheet_name="input_command", row=in_var.get("reserved_keyword") + 2, column_name="res1",
                                value=in_var.get("data"))
    return in_var
```