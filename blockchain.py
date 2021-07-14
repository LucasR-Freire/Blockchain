# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:17:54 2021

@author: Lucas
"""

# Module 1 - Create a Blockchain
#%% Importanti the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
#%% PART 1 - BUILDING A BLOCKCHAIN

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash}
        self.chain.append(block)
        return block

    def remove_block(self, index):
        self.chain.pop(index)

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()  
            if hash_operation.startswith('0'*4):
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
                
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() 
            if not hash_operation.startswith('0'*4) :
                return False
            previous_block = block
            block_index += 1
        return True
        
#%% PART 2 - MINING OUR BLOCKCHAIN

#%%      Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
#%%     Creating a Blockchain
aika = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = aika.get_previous_block()
    previous_proof = previous_block['proof']
    proof = aika.proof_of_work(previous_proof)
    previous_hash = aika.hash(previous_block)
    block = aika.create_block(proof, previous_hash)
    response = {'message': 'Congratulation, you just mined a block!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200
    
#%% Mining a new block
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain':aika.chain,
                'lenght': len(aika.chain)} 
    return jsonify(response), 200
#%% Validating of the Blockchain
@app.route('/is_valid',methods=['GET'])
def is_valid():
    previous_block = aika.chain[0]
    block_index = 1
    while block_index < len(aika.chain):
        block = aika.chain[block_index]
        if block['previous_hash'] != aika.hash(previous_block):
            response = 'The Blockchain is not valid.'
            break
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest() 
        if not hash_operation.startswith('0'*4) :
            response = 'The Blockchain is not valid.'
            break
        previous_block = block
        block_index += 1
        
    try:
        response
    except NameError:
        response = 'The Blockchain is valid.'
    return jsonify(response),200
#%% Running the app
app.run(host='0.0.0.0', port= 5000)








