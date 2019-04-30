#!/bin/bash

app_code="bk_template"
smart_root="/Users/kris/Storage/SAAS/"
smart_dir="${smart_root}${app_code}/"
src="${smart_dir}/src"
pkgs="${smart_dir}/pkgs"

mkdir -p $pkgs
cp app.yml $smart_dir

# 判断是否要执行pip download
if [[ "$2"x = "pip"x || -z "`ls $pkgs`" ]]; then
  pip download --no-binary=:all: -r requirements.txt --trusted-host pypi.douban.com -d $pkgs
fi

# 删除文件夹src
rm -rf $src

# 创建文件夹src
mkdir $src

# 排除文件夹node_modules和.git文件夹以及pyc文件
rsync -avz --exclude "node_modules*" --exclude ".git*" --exclude "*.pyc" . $src

# 设置s-mart应用版本信息
if [ -z $1 ]; then
    version="1.0.0"
else
    version=$1
fi

cd $smart_root
COPYFILE_DISABLE=1 tar -zcvf "${app_code}_V${version}.tar.gz" $app_code
