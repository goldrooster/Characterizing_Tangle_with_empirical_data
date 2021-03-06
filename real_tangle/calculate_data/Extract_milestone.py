import iota
import iotapy
import json

# For example, export milestone from MS7 raw dataset.
name = "MS12"

r = iotapy.storage.providers.rocksdb.RocksDBProvider(
        db_path='/home/xxiao/fyg-iota-vm/mainnetdb',
        db_log_path='/home/xxiao/fyg-iota-vm/mainnetdb.log',
        read_only=True
    )
r.init()

r.first('milestone')
print(r.first('milestone'))
genesis = []

def milestone_list(num):
    milestone = []

#Last milestone index933209
    while num <=61491:
        if num<=61491:
# First miilestone index
            if num == 18750:
                milestone_dict = {}
                milestone_dict["index"] = r.first("milestone")[0]
                milestone_dict['hash'] = str(r.first("milestone")[1][1])
                txh = iota.TransactionHash(str(r.first("milestone")[1][1]))
                column_family = 'transaction'
                tx = r.get(txh, column_family)
                milestone_dict['trunk_hash'] = str(tx.trunk_transaction_hash)
                milestone_dict['branch_hash'] = str(tx.branch_transaction_hash)
                milestone_dict['timestamp'] = str(tx.timestamp)
                milestone.append(milestone_dict)
                print(milestone_dict)

            else:
                milestone_dict = {}
                milestone_dict['index'] = r.next(num,'milestone')[0]
                milestone_dict['hash'] = str(r.next(num,'milestone')[1][1])
                txh = iota.TransactionHash(str(r.next(num,'milestone')[1][1]))
                column_family = 'transaction'
                tx = r.get(txh, column_family)
                milestone_dict['trunk_hash'] = str(tx.trunk_transaction_hash)
                milestone_dict['branch_hash'] = str(tx.branch_transaction_hash)
                milestone_dict['timestamp'] = str(tx.timestamp)
# Genesis milestone branch_hash is all9
                if str(tx.branch_transaction_hash) == "999999999999999999999999999999999999999999999999999999999999999999999999999999999":
                    genesis.append(milestone_dict)
                    print('genesis',milestone_dict)
                print(milestone_dict)
                milestone.append(milestone_dict)
            num = num + 1



    #
        with open("{n}_milestone_dict.json".format(n = name),"w") as f:
            json.dump(milestone,f)
        #f.flush()
    with open("{n}_genesis_dict.json".format(n = name),"w") as f:
        json.dump(genesis,f)
        #f.flush()

    return milestone

milestone_list(18750)

