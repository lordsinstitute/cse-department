import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">Spam Detection for Smart Home Devices using Machine Learning</h1>
        
        <div className="bg-white p-8 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-6">Abstract</h2>
          <p className="mb-6 text-gray-700 leading-relaxed">
            The Internet of Things (IoT) is a group of millions of devices having sensors and actuators linked over wired or wireless channels for data transmission. IoT has grown rapidly over the past decade with more than 25 billion devices expected to be connected by 2020. The volume of data released from these devices will increase many-fold in the years to come. In addition to an increased volume, the IoT devices produce a large amount of data with a number of different modalities having varying data quality defined by its speed in terms of time and position dependency. In such an environment, machine learning (ML) algorithms can play an important role in ensuring security and authorization based on biotechnology, anomalous detection to improve the usability, and security of IoT systems. On the other hand, attackers often view learning algorithms to exploit the vulnerabilities in smart IoT-based systems. Motivated from these, in this article, we propose the security of the IoT devices by detecting spam using ML.
          </p>
          
          <div className="flex space-x-4 justify-center mt-8">
            <Link href="/admin" className="btn btn-primary">
              Admin Login
            </Link>
            <Link href="/user" className="btn btn-primary">
              User Login
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
} 