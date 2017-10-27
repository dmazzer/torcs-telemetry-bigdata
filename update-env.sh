#!/bin/bash

echo "Gerando chaves SSH para o Haddop"
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys


echo "Atualizando repositórios"
git config --global alias.up '!git remote update -p; git merge --ff-only @{u}'
git checkout master && git up
