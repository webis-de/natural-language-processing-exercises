#!/usr/bin/sh

zcat /mnt/ceph/storage/corpora/corpora-thirdparty/corpus-clueweb12/corpus-waterloo-spam-cw12/waterloo-spam-cw12-decoded/* |shuf |head -1000 > cw12-spam-ranks

