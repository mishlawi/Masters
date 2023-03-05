const prompt = require('prompt-sync')({ sigint: true })
const path = require('path')
const fs = require('fs')
const cryptojs = require("crypto-js")
const crypto = require("crypto")
const sss = require('shamirs-secret-sharing')


const deposit = async () => {

    console.log('Enter the filename: ')
    let file = prompt('> ')

    let data
    let extension = path.extname(file)

    if (extension == '.pdf') {
        pdffile = fs.readFileSync(file)
        data = pdffile.toString('binary')
    }
    else {
        data = fs.readFileSync(file, 'utf8')
    }

    const file_hash = cryptojs.SHA256(data).toString()
    
    let to_share = ''
    while (to_share != 'y' && to_share != 'n') {
        console.log('Do you want this file to be accessed by more than one person? y/n ')
        to_share = prompt('> ')
    }

    try {

        const key = crypto.generateKeySync("aes", { length: 128, })

        const IV = cryptojs.enc.Hex.parse(crypto.randomBytes(16).toString('hex'))
        const encrypted_file = cryptojs.AES.encrypt(data, key, {
            iv: IV
        })

        const file_hash_encrypted = file_hash + ':' + encrypted_file.toString() + "," + encrypted_file.iv + ';' + extension

        const secret = key.export().toString('hex')

        if (to_share == 'y') {
            console.log('Enter the names of the users that are allowed to access this file (separated by spaces): ')
            let users_allowed = prompt('> ').split(' ')

            console.log('Enter the public keys of the users that are allowed to access this file (separated by spaces in the same order as their emails): ')
            let users_allowed_keys = prompt('> ').split(' ')

            while (users_allowed.length != users_allowed_keys.length) {
                console.log('The number of public keys differ from the number of emails.\nPlease try again.');

                console.log('Enter the names of the users that are allowed to access this file (separated by spaces): ')
                users_allowed = prompt('> ').split(' ')

                console.log('Enter the public keys of the users that are allowed to access this file (separated by spaces in the same order as their emails): ')
                users_allowed_keys = prompt('> ').split(' ')
            }

            console.log('Enter the minimum number of users that can access together (it cannot be only one person!): ')
            let min = parseInt(prompt('> '))

            while (min <= 1) {
                console.log('Enter the minimum number of users that can access together (it cannot be only one person!): ')
                min = parseInt(prompt('> '))
            }

            const shares = sss.split(secret, { shares: users_allowed.length, threshold: min })

            for (var i = 0; i < users_allowed.length; i++) {
                const encrypted_part = crypto.publicEncrypt(
                    {
                        key: fs.readFileSync(users_allowed_keys[i], { encoding: 'utf-8' }),
                        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
                        oaepHash: 'sha256',
                    },
                    Buffer.from(shares[i], 'base64')
                )

                let m = file.match(/(.*)\.\w+/)
                fs.writeFileSync(m[1] + 'hash' + users_allowed[i] + '.txt', JSON.stringify({ hash: file_hash, part_of_key: encrypted_part.toString('hex') }) + '\n')
            }
        }
        else if (to_share == 'n') {

            console.log('Enter your public key file: ')
            const user_public_key = fs.readFileSync(prompt('> '), { encoding: 'utf-8' })

            const encrypted_key = crypto.publicEncrypt(
                {
                    key: user_public_key,
                    padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
                    oaepHash: 'sha256',
                },
                Buffer.from(secret)
            )

            let m = file.match(/(.*)\.\w+/)
            fs.writeFileSync(m[1] + 'hash' + '.txt', JSON.stringify({ hash: file_hash, key: encrypted_key.toString('hex') }) + '\n', 'utf8')
        }


        fs.appendFileSync('files.txt', file_hash_encrypted + '\n')


    } catch (err) {
        console.error(err)
    }
}


const get = () => {

    console.log('Enter the file hash: ')
    let file_hash = prompt('> ')

    const files_data = fs.readFileSync('files.txt', 'utf-8')
    let encrypted_file = ''
    let IV = ''
    let extension = ''
    files_data.split('\n').forEach(line => {
        const hash_line = line.split(':')[0]
        if (hash_line == file_hash) {
            encrypted_file = line.split(':')[1].split(",")[0]
            IV = cryptojs.enc.Hex.parse(line.split(':')[1].split(",")[1].split(';')[0])
            extension = line.split(':')[1].split(",")[1].split(';')[1]
        }
    })
    if (encrypted_file != '' || IV != '') {
        console.log('Enter parts separated by spaces or the entire encrypted key if it was not shared:')
        let parts = prompt.hide('>').split(' ')

        console.log('Enter the private keys separated by spaces in the same order as the parts:')
        let priv_keys = prompt('>').split(' ')

        while (parts.length != priv_keys.length) {
            console.log('The number of parts differ from the number of private keys entered.\nPlease try again.');

            console.log('Enter parts separated by spaces or the entire encrypted key if it was not shared:')
            parts = prompt.hide('>').split(' ')

            console.log('Enter the private keys separated by spaces in the same order as the parts:')
            priv_keys = prompt('>').split(' ')
        }


        let decrypted_parts = []

        try {
            for (var i = 0; i < parts.length; i++) {
                console.log(`Enter the passphrase for the #${i + 1} private key entered:`)
                const pass = prompt.hide('> ')

                decrypted_parts[i] = crypto.privateDecrypt(
                    {
                        key: fs.readFileSync(priv_keys[i], 'utf-8'),
                        passphrase: pass,
                        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
                        oaepHash: 'sha256',
                    },
                    Buffer.from(parts[i], 'hex')
                )
            }

            let recovered_key = ''
            if (parts.length > 1) {
                recovered_key = sss.combine(decrypted_parts)
            }
            else {
                recovered_key = decrypted_parts[0]
            }

            const decrypted_file = cryptojs.AES.decrypt(encrypted_file, recovered_key, {
                iv: IV
            })

            if(extension == '.pdf'){
                const data = Buffer.from(decrypted_file.toString(cryptojs.enc.Utf8),'binary')
                fs.writeFileSync('decrypted' + extension, data)
                console.log(`Decryption succeeded! Check the result file: decrypted${extension}`)
            }
            else{
                fs.writeFileSync('decrypted' + extension, decrypted_file.toString(cryptojs.enc.Utf8))
                console.log(`Decryption succeeded! Check the result file: decrypted${extension}`)
            }
            
            
        } catch (err) {
            console.error(err);
            console.error("There was an error decrypting the file! Maybe your password was wrong, or the decipher key isn't complete.\n")
        }
    } else {
        console.log('There is no stored file with such hash!\n');
    }

}


const main = async () => {

    console.log("Choose one option:\n1 - Deposit file\n2 - Get file\n0 - Leave\n")
    let choice = prompt("> ")

    while (choice != '0') {

        if (choice == '1') {
            await deposit()
        }
        else if (choice == '2') {
            get()
        }

        console.log("\n\nChoose one option:\n1 - Deposit file\n2 - Get file\n0 - Leave\n")
        choice = prompt("> ")
    }

}

main()