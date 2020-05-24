#/bin/bash
git config --global user.email 'wykeith@gmail.com'
git config --global user.name 'wykeith'

git config --global filter.openssl.smudge ~/tools/smudge_filter_openssl
git config --global filter.openssl.clean ~/tools/clean_filter_openssl
git config --global diff.openssl.textconv ~/tools/diff_filter_openssl

cat <<EOF > .gitattributes
*.ipynb filter=openssl diff=openssl
[merge]
    renormalize = true
EOF

#export PASS_FIXED = "password"

