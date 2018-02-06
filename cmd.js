import subprocess;

var return_code = subprocess.call('sudo python bh1750.py a b', shell=True);
console.log(return_code);
