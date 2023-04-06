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

### Creating Transactions

Transactions require the sum of the inputs to be greater than or equal to the sum of the outputs. Similarly, transactions require a ScriptSig that, when combined with the ScriptPubKey, are valid.

To create a transaction, we need at least one output we’ve received. That is, we need an output from the UTXO set whose ScriptPubKey we can unlock.

The construction of a transaction requires answering some basic questions:

- Where do we want the bitcoins to go?

- What UTXOs can we spend?

- How quickly do we want this transaction to get into the blockchain?

## Blocks

Transactions transfer bitcoins from one party to another and are unlocked, or authorized, by signatures. This ensures that the sender authorized the transaction, but what if the sender sends the same coins to multiple people? This is called the double-spending problem.

Much like being given a check that has the possibility of bouncing, the receiver needs to be assured that the transaction is valid.

This is where a major innovation of Bitcoin comes in, with blocks. Think of blocks as a way to order transactions. If we order transactions, a double-spend can be prevented by making any later, conflicting transaction invalid. This is the equivalent to accepting the earlier transaction as the valid one.

Implementing this rule would be easy (earliest transaction is valid, subsequent transactions
that conflict are invalid) if we could order transactions one at a time. Unfortunately,
that would require nodes on the network to agree on which transaction is supposed to be next and would cause a lot of transmission overhead in coming to
consensus.

We could also order large batches of transactions, maybe once per day, but that wouldn’t be very practical as transactions would settle only once per day and not
have finality before then.

Bitcoin finds a middle ground between these extremes by settling every 10 minutes in batches of transactions. These batches of transactions are what we call blocks.

### Coinbase Transaction

Coinbase is the required first transaction of every block and is the only transaction allowed to bring bitcoins into existence. The coinbase transaction’s outputs are kept by whomever the mining entity designates and usually include all the transaction fees of the other transactions in the block as well as something called the block reward.

The transaction structure is no different from that of other transactions on the Bitcoin network, with a few exceptions:

 - Coinbase transactions must have exactly one input.

 - The one input must have a previous transaction of 32 bytes of 00.

 - The one input must have a previous index of ffffffff.

These three conditions determine whether a transaction is a coinbase transaction or not.
