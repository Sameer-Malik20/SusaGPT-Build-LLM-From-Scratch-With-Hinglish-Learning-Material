# 🛠️ Project 3: Distributed DB with Docker
> **Objective:** Setup a distributed database cluster (CockroachDB) locally using Docker to understand replication, sharding, and high availability | **Difficulty:** Expert | **Target:** SRE & Infrastructure Engineers

---

## 🎯 1. The Challenge
Aapko ek "Survivable Database Cluster" banana hai. Maan lijiye aapke paas 3 nodes hain. Agar ek node down hota hai, toh bhi database chalta rehna chahiye bina kisi data loss ke.

### Tools:
- Docker & Docker Compose
- CockroachDB (The world's leading NewSQL database)

---

## 🏗️ 2. The Setup (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  node-1:
    image: cockroachdb/cockroach:v23.1.8
    command: start --insecure --join=node-1,node-2,node-3
    ports:
      - "26257:26257"
      - "8080:8080"
  node-2:
    image: cockroachdb/cockroach:v23.1.8
    command: start --insecure --join=node-1,node-2,node-3
  node-3:
    image: cockroachdb/cockroach:v23.1.8
    command: start --insecure --join=node-1,node-2,node-3
```

---

## 💻 3. Implementation Steps

### Step 1: Launch the Cluster
```bash
docker-compose up -d
# Initialize the cluster
docker exec -it node-1 ./cockroach init --insecure
```

### Step 2: Verify High Availability
1. Open the Dashboard at `http://localhost:8080`. You should see 3 nodes.
2. Insert some data:
   ```bash
   docker exec -it node-1 ./cockroach sql --insecure -e "CREATE TABLE test (id INT PRIMARY KEY, val TEXT); INSERT INTO test VALUES (1, 'Hello Distributed World');"
   ```
3. **The Kill Test:** Stop one node: `docker-compose stop node-2`.
4. **The Verification:** Try to read the data from `node-3`:
   ```bash
   docker exec -it node-3 ./cockroach sql --insecure -e "SELECT * FROM test;"
   ```
   *Data should still be there!*

---

## ⚡ 4. Advanced Tasks (Distributed Deep Dive)
1. **Replication Factor:** Change the replication factor from 3 to 5 and explain why we use odd numbers.
2. **Global Simulation:** Use Docker network latency to simulate nodes being in different countries and measure the "Write Latency".
3. **Partitioning:** Design a table that is automatically sharded across these 3 nodes.

---

## 🌍 5. Real-World Vision
Ye bilkul waisa hi setup hai jaisa **Netflix** ya **DoorDash** use karte hain apne production data centers mein. Cluster ke nodes alag-alag buildings (Availability Zones) mein hote hain.

---

## ✅ 6. Evaluation Criteria
- [ ] Cluster successfully initialized with 3 nodes.
- [ ] Database remained functional after stopping one node.
- [ ] Understood the role of the "Gossip Protocol" in node discovery.
- [ ] Correctly explained the "Quorum" (Majority) principle.

漫
---

## 🚀 7. Bonus: The "Chaos" Challenge
"Run a heavy write loop in a script and stop nodes one by one until the database finally stops responding. Find the 'Minimum nodes required' to stay alive."
漫
