const dfd = require("danfojs-node")
console.log('\x1b[32m%s\x1b[0m', "Loading dataset for decryption...")
dfd.readCSV("/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/cleaned.csv")
  .then(df => {
  
  function recordingDataToTemperatureArray(recordingData) {
    var hexString = base64ToHex( recordingData.base64?recordingData.base64:recordingData );
    var byteArray = [];
    for (var l=0; l<hexString.length; l+=2) {
      byteArray.push("0x" + hexString.substr(l, 2));
    }
    var temperatures = [];
    for (var l=0; l<byteArray.length; l+=2) {
      temperatures.push( byteToRecordingTemp(byteArray[l], byteArray[l+1]) );
    }
    return temperatures
  }

  
  function base64ToHex(str) {
    for (var i = 0, bin = atob(str.replace(/\s/g, "")), hex = []; i < bin.length; ++i) {
      var tmp = bin.charCodeAt(i).toString(16);
      if (tmp.length === 1) tmp = "0" + tmp;
      hex[hex.length] = tmp;
    }
    return hex.join("");
  }
  
  function byteToRecordingTemp(tempByte, tempByte2) {
    var recordingInt = 0;
    recordingInt = (recordingInt << 8) | tempByte2;
    recordingInt = (recordingInt << 8) | tempByte;
  
    var bigBits = 0;
    var littleBits = 0;
    bigBits =  (recordingInt >> 10) & 0x003f;
    littleBits = (recordingInt >> 0) & 0x03ff;
  
    var retNumber = (bigBits * 1000) + littleBits;
    return retNumber;
  }

//console.log(df.shape[0])

all = df.shape[0]
batch_size = 450000
out_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted/"
let spl = Math.floor(df.shape[0]/batch_size)
let j = 0
for (let i = 1; i <= spl; i+=1){
  start = j;
  end = i*batch_size;
  id = "decrypted" + i;
  rng = start+":"+end
  let sub_df = df.iloc({rows: [rng]})
  let new_col = sub_df['Data'].apply(recordingDataToTemperatureArray, { axis: 1 })
  sub_df.addColumn("Data", new_col, { inplace: true})
  dfd.toCSV(sub_df, { filePath: out_file+id});

  console.log('\x1b[33m%s\x1b[0m', "Decrypted range: "+rng, "\n")

  j = j+batch_size
}

if (all - (spl*batch_size) > 0){
  start = spl*batch_size
  end = all
  id = "decrypted last";
  rng = start+":"+end
  let sub_df = df.iloc({rows: [rng]})
  let new_col = sub_df['Data'].apply(recordingDataToTemperatureArray, { axis: 1 })
  sub_df.addColumn("Data", new_col, { inplace: true})
  dfd.toCSV(sub_df, { filePath: out_file+id});
  console.log('\x1b[33m%s\x1b[0m', "Decrypted range: "+rng, "\n")
}

console.log('\x1b[43m%s\x1b[0m', "Data decryption ended");

  }).catch(err=>{
    console.log(err);
 })
 
