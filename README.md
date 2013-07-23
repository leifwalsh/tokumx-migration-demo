tokumx-migration-demo
=====================

[TokuMX][1] is a replacement for MongoDB that changes all the storage code
for better performance, concurrency, and compression.  Because the data
format is different than in MongoDB, migration requires a full
dump-and-reload, and because the replication format is different, it can
be hard to migrate a live production system.

In TokuMX 1.0.3, we are introducing a tool to make this process easier.
It replays a vanilla MongoDB replication oplog on TokuMX.  This makes the
migration process much simpler, more seamless, and it can be done with
next to no downtime.

This repo contains an executable presentation that I recorded using
[ascii.io][2], a really cool screencast service.

You can view the full recording at http://ascii.io/a/4285.  You can also
clone this repo, read it, and follow along as you walk through the process
yourself, in a terminal or using [Babel][3].

[1]: http://www.tokutek.com/products/tokumx-for-mongodb/
[2]: http://ascii.io/
[3]: http://orgmode.org/worg/org-contrib/babel/

Thanks
------

Big thanks to @mongodb for building MongoDB, the
[org-mode contributors][4] for creating the best emacs mode, and @sickill
for building ascii.io.

[4]: http://orgmode.org/org.html#History-and-Acknowledgments
