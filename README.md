# Bitcoin

## Transactions

At a high level, transaction has 4 components:

- **version** - shows which additional features the transaction uses.

- **inputs** - defines what bitcoins are being spent.

    Each input needs two things:
    
    - A reference to bitcoins you received previously

    - Proof that these are yours to spend (uses ECDSA)

    Each input contains four fields. The first two fields point to the previous transaction output and the last two fields define how the previous transaction output can be spent. The fields are as follows:

    - Previous transaction ID (the hash256 of the previous transaction’s contents)

    - Previous transaction index (since previous transaction may have many outputs, it needs to define exactly which output within a transaction will be spent. It is captured with this part)
    
    - ScriptSig (it has to do with Bitcoin’s smart contract language)
    
    - Sequence (it is currently used with Replace-By-Fee (RBF) and OP_CHECKSEQUENCEVERIFY)

- **outputs** - defines where the bitcoins are going.

- **locktime** - defines when the transaction starts being valid.

## Script

The ability to lock and unlock coins is the mechanism by which bitcoin is transferred.

Locking is giving some bitcoins to some entity. Unlocking is spending some bitcoins that you have received.

This locking/unlocking mechanism, which is often called a smart contract. “Smart contract” is a fancy way of saying “programmable,” and the “smart contract language” is simply a programming language. In Bitcoin, Script is the smart contract language, or the programming language used to express the conditions under which bitcoins are spendable.

Transactions assign bitcoins to a locking script. The locking script is what’s specified in the ScriptPubKey field.

The unlocking of the lockbox is done in the ScriptSig field.

## Transaction Creation and Validation

Every node, when receiving transactions, makes sure that each transaction adheres to the network rules. This process is called transaction validation.

The main things that a node checks:

- The inputs of the transaction are previously unspent (prevents double-spending).

    This can be checked by any full node by looking at the UTXO set.

    A full node can check the spentness of an input pretty easily, but a light client has to get this information from someone else.

- The sum of the inputs is greater than or equal to the sum of the outputs (makes sure no new bitcoins are created, except a coinbase transaction).

    Since inputs don’t have an amount field, this must be looked up on the blockchain. Once again, full nodes have access to the amounts associated with the unspent output, but light clients have to depend on full nodes to supply this information.

- The ScriptSig successfully unlocks the previous ScriptPubKey (makes sure that the combien scripti is valid).

