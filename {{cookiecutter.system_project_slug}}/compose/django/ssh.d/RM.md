# 访问密钥配置

```
├── ssh.d
│   ├── RM.md
│   ├── config
│   ├── id_rsa
│   └── id_rsa.pub
```

```
$ cat ssh.d/config
Host repository.domain.com
User your-username@repository.domain.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa
```
