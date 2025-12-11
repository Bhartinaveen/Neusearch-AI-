import { Link } from 'react-router-dom'
import { ShoppingBag, MessageCircle } from 'lucide-react'

export default function Navbar() {
    return (
        <nav className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-50">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <Link to="/" className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <ShoppingBag className="w-6 h-6 text-brand-600" />
                    Neusearch AI
                </Link>
                <div className="flex items-center gap-4">
                    <button className="text-slate-600 hover:text-brand-600 transition-colors">
                        <MessageCircle className="w-6 h-6" />
                    </button>
                </div>
            </div>
        </nav>
    )
}
