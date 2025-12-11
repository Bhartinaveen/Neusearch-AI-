import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import { motion } from 'framer-motion'
import { ArrowLeft, Check, Share2 } from 'lucide-react'

interface Product {
    id: number
    title: string
    price: string
    description: string
    features: Record<string, string>
    image_url: string
    category: string
    link: string
}

export default function ProductDetail() {
    const { id } = useParams()
    const [product, setProduct] = useState<Product | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get(`${import.meta.env.VITE_BACKEND_URL}/products/${id}`)
            .then(res => setProduct(res.data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false))
    }, [id])

    if (loading) return <div className="text-center py-20">Loading...</div>
    if (!product) return <div className="text-center py-20">Product not found</div>

    return (
        <div className="max-w-6xl mx-auto">
            <Link to="/" className="inline-flex items-center text-slate-500 hover:text-slate-900 mb-6">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Products
            </Link>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="aspect-[4/3] bg-slate-100 rounded-2xl overflow-hidden"
                >
                    <img
                        src={product.image_url || 'https://placehold.co/800x600'}
                        alt={product.title}
                        className="w-full h-full object-cover"
                    />
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                >
                    <div className="mb-6">
                        <span className="inline-block px-3 py-1 bg-brand-50 text-brand-600 rounded-full text-sm font-medium mb-3">
                            {product.category}
                        </span>
                        <h1 className="text-3xl font-bold text-slate-900 mb-4">{product.title}</h1>
                        <p className="text-4xl font-bold text-slate-900 mb-6">{product.price}</p>
                        <p className="text-slate-600 leading-relaxed mb-8">{product.description}</p>

                        <div className="flex gap-4 mb-8">
                            <a
                                href={product.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex-1 bg-slate-900 text-white text-center py-4 rounded-xl font-semibold hover:bg-slate-800 transition-colors"
                            >
                                Rent Now
                            </a>
                            <button className="p-4 border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors">
                                <Share2 className="w-6 h-6 text-slate-600" />
                            </button>
                        </div>

                        <div className="border-t border-slate-200 pt-8">
                            <h3 className="font-semibold text-slate-900 mb-4">Key Features</h3>
                            <div className="grid grid-cols-2 gap-4">
                                {Object.entries(product.features).map(([key, value]) => (
                                    <div key={key} className="flex items-start gap-3">
                                        <div className="mt-1 w-5 h-5 rounded-full bg-green-50 flex items-center justify-center flex-shrink-0">
                                            <Check className="w-3 h-3 text-green-600" />
                                        </div>
                                        <div>
                                            <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{key}</p>
                                            <p className="text-slate-900">{value}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    )
}
