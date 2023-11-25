#!/usr/bin/sh

cat /mnt/ceph/storage/corpora/corpora-thirdparty/corpus-clueweb09/spam-ranks/clueweb09spam.Fusion |shuf |head -1000 > cw09-spam-ranks

