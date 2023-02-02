const dfd = require("danfojs-node")
console.log('\x1b[32m%s\x1b[0m', "Loading dataset for decryption...")
dfd.readCSV("/home/ev22335/bbt_research/data/decrypted.csv")
  .then(df => {

    console.log(df.shape[0])
  }).catch(err=>{
    console.log(err);
 })
 