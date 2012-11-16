# OpenWrt documentation scripts

For more documenation read:

https://github.com/mcgrof/openwrt-doc-scripts

These scripts are to be used to help enhance OpenWrt's documentation.
There are two targets a main release page for each release and then
one page for each package. The main release page output is sent to
stdout and the individual packages have a file written to in the
specified output directory.

# OpenWrt Releases

We'll start documenting these release:

  * Attitude Adjustment - AA-12.09-beta2

This git tree has scripts to update the wiki page for the above
release along with generating documentation for each package.
The page documentation is sent to stdout and individual package
documenation is written to the output directory. The stdout can
be read to your clipboard for your web browser using the commands
specified below.

# Updating OpenWrt documentation

Target wiki page:

  * http://wiki.openwrt.org/doc/devel/packages/list

Commands to use to update:

./scripts/package-iter-openwrt.py -p Packages/AA-12.09-beta2 -l opkg-list-installed/AA-12.09-beta2/db120 -o html | xclip -sel clip

The Packages file came from:

  * http://downloads.openwrt.org/attitude_adjustment/12.09-beta2/ar71xx/generic/packages/Packages

# Package documentation

# Sending patches

Please send me patches/feedback for this script to:

  * mcgrof@do-not-panic.com

Be sure to Cc:

  * openwrt-devel@lists.openwrt.org
