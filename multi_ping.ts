import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
const BASE_IP = "172.31";

async function pingNetwork(baseIp: string = BASE_IP, target: string = "1", targetRange: string = "1-6", count: number = 30) {
    async function pingIp(ip: string): Promise<string> {
        try {
            const command = `ping -c ${count} ${ip}`;
            const { stdout } = await execAsync(command);
            
            const lossRateMatch = stdout.match(/(\d+(\.\d+)?)% packet loss/);
            if (lossRateMatch) {
                return `${ip} - Packet Loss Rate: ${parseFloat(lossRateMatch[1])}%`;
            } else {
                return `${ip} - Failed to retrieve packet loss rate`;
            }
        } catch (error) {
            return `Error pinging ${ip}: ${error.message}`;
        }
    }

    const targetIps = target.split('-').map(Number);
    const startIp = targetIps[0];
    const endIp = targetIps.length > 1 ? targetIps[1] : startIp;

    const targetRangeValues = targetRange.split('-').map(Number);
    const startTr = targetRangeValues[0];
    const endTr = targetRangeValues.length > 1 ? targetRangeValues[1] : startTr;

    const ipList: string[] = [];
    for (let targetIp = startIp; targetIp <= endIp; targetIp++) {
        for (let x = startTr; x <= endTr; x++) {
            ipList.push(`${baseIp}.${targetIp}.${x}`);
        }
    }

    for (let targetIp = startIp; targetIp <= endIp; targetIp++) {
        console.log(`Pinging IPs ${baseIp}.${targetIp}.x (x = ${startTr} to ${endTr}), ${count} times each...`);
    }

    const results = await Promise.all(ipList.map(ip => pingIp(ip)));

    let err = false;
    results.forEach(result => {
        console.log(result);
        if (result.includes('Packet Loss Rate') && parseFloat(result.split(': ')[1]) > 0) {
            err = true;
        }
    });

    if (!err) {
        console.log("All passed!");
    }
}

// Example usage:
const startTime = Date.now();
pingNetwork("192.168", "0", "1-6", 10).then(() => {
    const endTime = Date.now();
    console.log(`Total time taken: ${(endTime - startTime) / 1000} seconds`);
}).catch(err => {
    console.error(err);
});