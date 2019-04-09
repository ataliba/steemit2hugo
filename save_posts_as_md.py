#!/usr/bin/python
# -*- coding: utf-8 -*-

from beem import Steem
from beem.comment import Comment
from beem.account import Account
import os
import io
import argparse
import markdown 
from mdx_bleach.extension import BleachExtension


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("author")
    parser.add_argument("path")
    args = parser.parse_args()
    author = args.author
    path = args.path
    stm = Steem(node="https://api.steemit.com")
    account = Account(author, steem_instance=stm)
    for comment in account.get_blog(limit=500):
        if comment["author"] != author:
            continue
        markdown_content = comment.body
        title = comment.title
        timestamp = comment.json()["created"]
        author = comment["author"]
        permlink = comment["permlink"]
	# change the username to your user on steemit like @username @ataliba
        link_for_post='https://steemit.com/@username/'+permlink
        post_final='---\n'+'<br />**Postado originalmente na rede Steemit: ['+link_for_post+']('+link_for_post+')** <br /> \n----'
        yaml_prefix = '---\n'
        TitleYaml = title.replace(':', '')
        TitleYaml = TitleYaml.replace('\'', '')
        TitleYaml = TitleYaml.replace('#', '')
        TitleYaml = TitleYaml.replace('(', '')
        TitleYaml = TitleYaml.replace(')', '')
        yaml_prefix += 'title: %s\n' % TitleYaml
        yaml_prefix += 'date: %s\n' % timestamp
        yaml_prefix += 'permlink: /steemit/%s \n' % permlink
        yaml_prefix += 'type: posts \n'
        yaml_prefix += 'categories: [ "Steemit" ] \n'
        yaml_prefix += 'author: %s\n---\n' % author
        filename = os.path.join(path, timestamp.split('T')[0] + '_' + permlink + ".md")
       
        with io.open(filename, "w", encoding="utf-8") as f:
            f.write(yaml_prefix + markdown_content + post_final)

