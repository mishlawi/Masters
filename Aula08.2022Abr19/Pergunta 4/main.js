
// The constructor has the following properties

// index:
// This property is optional and tells you where the block sits on the chain.
//
// timestamp:
// As the name indicates, this property assigns a time stamp to the block that is created.
//
// data:
// This property stores any type of data that you might want to store like currency transactions such as how much money was transferred and who was the sender and recipient.
// You can also store other types of data like energy consumption, dog names, etc.
//
// previousHash:
// We create a previousHash property that contains a string that stores the hash value of the previous block.


const SHA256 =  require('crypto-js/sha256');

class Block{

    constructor (index, timestamp, data, previousHash = ''){
        
     
        this.index = index; //  This property is optional and tells you where the block sits on the chain.
        this.timestamp = timestamp; // this property assigns a time stamp to the block that is created.
        this.data = data; // stores any type of data that you might want to store like currency transactions 
        this.previousHash = previousHash; // contains a string that stores the hash value of the previous block.
        //property called hash
        this.hash = this.calculateHash();
    }
  
    //new function to calculate the hash of the block
     calculateHash(){
        return SHA256(this.index + this.previousHash + this.timestamp + JSON.stringify(this.data)).toString();
    }

    // The first block on the blockchain is called a genesis block.


}


class Blockchain{

    
    constructor(){
    this.chain = [this.createGenesisBlock()];
    }   

    createGenesisBlock(){

    // deixei o nome que dei à nossa blockchain, apesar do pedido ser Bloco inicial da koreCoin :)
    
    return new Block(0, "03/05/2022", "Bloco incial da myBlockChain", "0");
    }

    getlatestBlock(){
    return this.chain[this.chain.length - 1];
    }

    addBlock(newBlock){
    newBlock.previousHash = this.getlatestBlock().hash;
    newBlock.hash = newBlock.calculateHash();
    this.chain.push(newBlock);
    }

    //The most important property of the blockchain is it’s immutability.
    //We use this method to verify the integrity of the blockchain

    isChainValid(){
        for(let i = 1; i < this.chain.length; i++){
            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i-1];
            
            if(currentBlock.hash !== currentBlock.calculateHash()){
                return false;
            } //check for hash calculations
            
            if(currentBlock.previousHash !== previousBlock.hash){
                return false;
            } //check whether current block points to the correct previous block
            
        }
        
         return true;
    }
    
}

let  myBlockChain  = new Blockchain()
//adding blocks to the blockchain
myBlockChain.addBlock(new Block (1, "01/01/2018", {amount: 20}));
myBlockChain.addBlock(new Block (2, "02/01/2018", {amount: 40}));
myBlockChain.addBlock(new Block (3, "02/01/2018", {amount: 40}));

//log data that myBlockChain returns on the console
console.log(JSON.stringify(myBlockChain, null, 4));


//Checking validity before tampering
console.log('Is Blockchain valid? ' + myBlockChain.isChainValid());

//tampering with blockchain by changing one of the earlier values
myBlockChain.chain[1].data = { amount: 100 };
//recalculating hash value
myBlockChain.chain[1].hash = myBlockChain.chain[1].calculateHash();

//Checking validity after tampering
console.log('Is Blockchain valid? ' + myBlockChain.isChainValid());



//novas transações

myBlockChain.addBlock(new Block (4, "01/05/2022", {amount: 87}));
myBlockChain.addBlock(new Block (5, "02/05/2022", {amount: 17}));
myBlockChain.addBlock(new Block (6, "03/05/2022", {amount: 123}));
myBlockChain.addBlock(new Block (7, "03/05/2022", {amount: 34}));