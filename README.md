![deployment](https://img.shields.io/github/deployments/scala-cn/scala-cn.github.io/github-pages?label=deployment) ![Platform](https://img.shields.io/badge/platform-Linux-8A2BE2) ![license](https://img.shields.io/github/license/scala-cn/scala-cn.github.io)

## 0. Table of Contents

* [Introduction](#1-introduction)
* [Code](#2-code)
* [Data](#3-data)
* [Defects Found](#4-defects-found)

## 1. Introduction

In this work, we present our long-term operation experience on a real-world production RDMA-based container network (RCN). We notice that the performance of RCN is significantly affected by the scale.
Through the careful telemetry analysis on our production RCN for a year, we find that the scalability walls are caused by the RCMA NICs (RNICs), whose hardware limits or defects siginificantly affect the performance when the RCN scales up.
However, we are confronted with a key challenge that we have very limited visbility into the internals of today's RNICs.

To address the problem, we propose a novel approach, i.e., **combinatorial causal testing**, to infer the most likely causes of the performance issues in RNICs based on the their common components and functionalities.
The resulting system, dubbed ScalaCN, is being gradually deployed in our production RCN, and has helped us to infer and resolve 82% causes of the RNICs' inferior performance.
Our evaluation on real-world workloads show that the end-to-end network bandwidth increases by 1.4× and the packet forwarding latency decreases by 31% after deploying ScalaCN.

## 2. Code

We have released the code for measurement, testing, and analysis in ScalaCN. The code is available at [scala-cn.github.io/scala-cn](https://github.com/scala-cn/scala-cn.github.io/tree/main/scala-cn).

The code is organized as follows:

<table>
  <tr>
    <td>Directory</td>
    <td>Description</td>
    <td>Source Code</td>
  </tr>
  <tr>
    <td rowspan='5'>common</td>
    <td rowspan='5'>common dependencies such as firmware tools, OVS tools, and tc tools</td>
    <td>mlx_resdump</td>
  </tr>
  <tr>
    <td >mlx_resdump_cpp</td>
  </tr>
  <tr>
    <td >data_path.py</td>
  </tr>
  <tr>
    <td >matcher.py</td>
  </tr>
  <tr>
    <td >tc.py</td>
  </tr>
  <tr>
    <td rowspan='2'>interpolation</td>
    <td rowspan='2'>performance fitting for RNICs</td>
    <td>interpolation_bw.py</td>
  </tr>
  <tr>
    <td>interpolation_bw.py</td>
  </tr>
  <tr>
    <td rowspan='2'>lib</td>
    <td rowspan='2'>static libs</td>
    <td>libibverbs.so.1.14.35.0</td>
  </tr>
  <tr>
    <td>libmlx5.so.1.19.35.0</td>
  </tr>
  <tr>
    <td rowspan='2'>testing</td>
    <td rowspan='2'>example code for combintorial testing and analysis</td>
    <td>data_parser.py</td>
  </tr>
  <tr>
    <td >profiling_cx7_ce_20_de_20.py</td>
  </tr>
  <tr>
    <td rowspan='4'>tracer</td>
    <td rowspan='4'>performance/state measurement and monitoring</td>
    <td>agent_tracer.py</td>
  </tr>
  <tr>
    <td>capture-tc.py</td>
  </tr>
  <tr>
    <td>table_flow_monitor.py</td>
  </tr>
  <tr>
    <td>tracer_config.py</td>
  </tr>
</table>

## 3. Data

The data samples in this work are available at [scala-cn.github.io/data](https://github.com/scala-cn/scala-cn.github.io/tree/main/data).
Each single data file regarding the RNIC performance on different component/functionality configurations is the output of the `perftest` tool.

An example of the data file is as follows:

```
---------------------------------------------------------------------------------------
                    RDMA_Write BW Test
 Dual-port       : OFF		Device         : [DEV]
 Number of qps   : 4		Transport type : IB
 Connection type : RC		Using SRQ      : OFF
 PCIe relax order: ON
 ibv_wr* API     : ON
 CQ Moderation   : 100
 Mtu             : 1024[B]
 Link type       : Ethernet
 GID index       : 3
 Max inline data : 0[B]
 rdma_cm QPs	 : OFF
 Data ex. method : Ethernet
---------------------------------------------------------------------------------------
 local address: LID 0000 QPN 0x06b8 PSN 0x74cf8c
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 local address: LID 0000 QPN 0x06b9 PSN 0xb9086
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 local address: LID 0000 QPN 0x06ba PSN 0xbe6e58
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 local address: LID 0000 QPN 0x06bb PSN 0x7eaac7
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 remote address: LID 0000 QPN 0x05d0 PSN 0x277fa8
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 remote address: LID 0000 QPN 0x05d1 PSN 0x29b472
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 remote address: LID 0000 QPN 0x05d2 PSN 0x69c1d4
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
 remote address: LID 0000 QPN 0x05d3 PSN 0xc29e93
 GID: 00:00:00:00:00:00:00:00:00:00:[IP]
---------------------------------------------------------------------------------------
 #bytes     #iterations    BW peak[MB/sec]    BW average[MB/sec]   MsgRate[Mpps]
 8388608    20000            9360.24            9360.24		   0.001170
---------------------------------------------------------------------------------------
```

## 4. Defects Found

We also report the RNICs' possible defects found during our measurement study.

| No.  | Symptom                            | Layer          | Ratio | Most Likely Cause                                            |
| ---- | ---------------------------------- | -------------- | ----- | ------------------------------------------------------------ |
| S1   | Repetitive flow re-offloading      | Virtual Switch | 17.1% | Flow entries in the RNIC are deleted although they are not aged. |
| S2   | Kernel stagnation                  | RNIC driver    | 5.9%  | The driver cannot handle the timeout of the RNIC's executing an operation. |
| S3   | Kernel crash on new flows          | RNIC driver    | 5.2%  | The driver frees a null pointer when the RNIC fails to create a flow entry. |
| S4   | Slow flow state maintenance        | RNIC hardware  | 11.4% | Flow deletion in the RNIC takes much longer (9×) time than expected. |
| S5   | Intermittent software forwarding   | RNIC hardware  | 15.3% | Flow counters are not updated timely. The virtual switch reads a "dirty" value. |
| S6   | Poor performance of specific flows | RNIC hardware  | 29.9% | Flow table query in the RNIC is performed sequentially in the on-chip memory. |
| S7   | PCIe link down when unbinding VFs  | RNIC hardware  | 8.4%  | Race condition emerges when the RNIC cleans up allocated resources. |
| S8   | RNIC unresponsiveness              | RNIC hardware  | 6.8%  | VXLAN encapsulation contexts exceed the RNIC's buffer capacity. |

