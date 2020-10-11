#/bin/bash
git config --global user.email 'wykeith@gmail.com'
git config --global user.name 'wykeith'

git config --global filter.openssl.smudge ~/tools/smudge_filter_openssl
git config --global filter.openssl.clean ~/tools/clean_filter_openssl
git config --global diff.openssl.textconv ~/tools/diff_filter_openssl
000
cat <<EOF > .gitattributes
*.ipynb filter=openssl diff=openssl
[merge]
    renormalize = true
EOF

echo """export PASS_FIXED = "password""""
read password
export PASS_FIXED=$password

git pull --all

git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.amend 'commit --amend -m'
git config --global alias.l 'log --name-only --oneline'
