import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { AnimatePresence, motion } from 'framer-motion'

interface Product {
    id: number
    title: string
    price: string
    image_url: string
    category: string
}

export default function Home() {
    const [products, setProducts] = useState<Product[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get(`${import.meta.env.VITE_BACKEND_URL}/products`)
            .then(res => setProducts(res.data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="text-center py-20">Loading...</div>

    return (
        <div>
            <h1 className="text-3xl font-bold mb-8">Featured Collection</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                    <Link key={product.id} to={`/product/${product.id}`} className="group">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow overflow-hidden border border-slate-100"
                        >
                            <div className="aspect-[4/3] bg-slate-100 relative overflow-hidden">
                                <img
                                    src={product.image_url || 'https://placehold.co/600x400'}
                                    alt={product.title}
                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                                />
                            </div>
                            <div className="p-4">
                                <p className="text-sm text-brand-600 font-medium mb-1">{product.category}</p>
                                <h3 className="font-semibold text-slate-900 mb-2 truncate">{product.title}</h3>
                                <p className="text-lg font-bold text-slate-900">{product.price}</p>
                            </div>
                        </motion.div>
                    </Link>
                ))}
            </div>
        </div>
    )
}
