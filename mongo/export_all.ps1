
$IFS=",";

# fill in your details here
$dbname='test_db'
$user='admin'
$pass='admin'
$host='localhost:27017'

# first get all collections in the database
$collections=`mongo "$host/$dbname" -u $user -p $pass --eval "rs.slaveOk();db.getCollectionNames();"`;
#collections=`mongo $dbname --eval "rs.slaveOk();db.getCollectionNames();"`;
$collectionArray=($collections);

# for each collection
for ((i=0; i<${#$collectionArray[@]}; ++i));
do
    echo 'exporting collection' ${collectionArray[$i]}
    # get comma separated list of keys. do this by peeking into the first document in the collection and get his set of keys
    keys=`.\mongo.exe "$host/$dbname" -u $user -p $pass --eval "rs.slaveOk();var keys = []; for(var key in db.${collectionArray[$i]}.find().sort({_id: -1}).limit(1)[0]) { keys.push(key); }; keys;" --quiet`;
    # now use mongoexport with the set of keys to export the collection to csv
    .\mongoexport.exe --host $host -u $user -p $pass -d $dbname -c ${collectionArray[$i]} --fields "$keys" --type=csv --out $dbname.${collectionArray[$i]}.csv;
done

