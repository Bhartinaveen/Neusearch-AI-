import { Github, Twitter, Linkedin, Mail } from 'lucide-react'

export default function Footer() {
    return (
        <footer className="bg-white border-t border-slate-200 mt-auto">
            <div className="container mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div className="col-span-1 md:col-span-1">
                        <h3 className="text-lg font-bold text-slate-900 mb-4">Neusearch AI</h3>
                        <p className="text-slate-600 text-sm mb-4 leading-relaxed">
                            Your AI-powered furniture shopping assistant. Find the perfect pieces for your home with intelligent semantic search.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-semibold text-slate-900 mb-4">Shop</h4>
                        <ul className="space-y-2 text-sm text-slate-600">
                            <li><a href="#" className="hover:text-brand-600 transition-colors">New Arrivals</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Living Room</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Bedroom</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Dining</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-slate-900 mb-4">Company</h4>
                        <ul className="space-y-2 text-sm text-slate-600">
                            <li><a href="#" className="hover:text-brand-600 transition-colors">About Us</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Careers</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Privacy Policy</a></li>
                            <li><a href="#" className="hover:text-brand-600 transition-colors">Terms of Service</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-slate-900 mb-4">Connect</h4>
                        <div className="flex gap-4">
                            <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Github className="w-5 h-5" /></a>
                            <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Twitter className="w-5 h-5" /></a>
                            <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Linkedin className="w-5 h-5" /></a>
                            <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Mail className="w-5 h-5" /></a>
                        </div>
                    </div>
                </div>

                <div className="pt-8 border-t border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p className="text-sm text-slate-500">© 2025 Neusearch AI. All rights reserved.</p>
                    <p className="text-sm text-slate-400 flex items-center gap-1">
                        Made by Naveen Bharti
                    </p>
                </div>
            </div>
        </footer>
    )
}
