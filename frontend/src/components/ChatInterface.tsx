import { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send, ShoppingBag, Mic, MicOff } from 'lucide-react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'

export default function ChatInterface() {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState<{ role: 'user' | 'bot', content: string, products?: any[] }[]>([
        { role: 'bot', content: "Hi! I can help you find the perfect furniture. Tell me what you're looking for?" }
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const [isListening, setIsListening] = useState(false)
    const scrollRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }, [messages])

    const startListening = () => {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Voice recognition is not supported in this browser.")
            return
        }

        const recognition = new (window as any).webkitSpeechRecognition()
        recognition.continuous = false
        recognition.interimResults = true
        recognition.lang = 'en-US'

        recognition.onstart = () => setIsListening(true)

        recognition.onresult = (event: any) => {
            let transcript = ''
            // Handle both interim and final results
            if (event.results && event.results.length > 0) {
                const result = event.results[event.resultIndex];
                transcript = result[0].transcript;
                setInput(transcript);
            }
        }

        recognition.onerror = (event: any) => {
            console.error(event.error)
            setIsListening(false)
        }

        recognition.onend = () => setIsListening(false)

        recognition.start()
    }

    const handleSend = async (manualInput?: string) => {
        const textToSend = manualInput || input
        if (!textToSend.trim()) return

        setMessages(prev => [...prev, { role: 'user', content: textToSend }])
        setInput("")
        setLoading(true)

        try {
            const res = await axios.post('http://localhost:8000/chat', { query: textToSend })
            setMessages(prev => [...prev, {
                role: 'bot',
                content: res.data.response,
                products: res.data.recommendations
            }])
        } catch (err) {
            setMessages(prev => [...prev, { role: 'bot', content: "Sorry, I encountered an error. Please try again." }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <>
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 bg-slate-900 text-white p-4 rounded-full shadow-lg hover:bg-brand-600 transition-colors z-50"
            >
                <MessageCircle className="w-6 h-6" />
            </button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 50, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 50, scale: 0.9 }}
                        className="fixed bottom-24 right-6 w-96 max-w-[calc(100vw-3rem)] h-[600px] bg-white rounded-2xl shadow-2xl border border-slate-200 z-50 flex flex-col overflow-hidden"
                    >
                        <div className="bg-slate-900 text-white p-4 flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <ShoppingBag className="w-5 h-5" />
                                <span className="font-semibold">Shopping Assistant</span>
                            </div>
                            <button onClick={() => setIsOpen(false)}><X className="w-5 h-5" /></button>
                        </div>

                        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50" ref={scrollRef}>
                            {messages.map((msg, i) => (
                                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-[85%] rounded-2xl p-3 ${msg.role === 'user' ? 'bg-brand-100 text-slate-900' : 'bg-white border border-slate-200 text-slate-800'
                                        }`}>
                                        <p className="text-sm">{msg.content}</p>
                                        {msg.products && (
                                            <div className="mt-3 space-y-2">
                                                {msg.products.map((p: any) => (
                                                    <Link to={`/product/${p.id || p.link}`} key={p.id || p.link} className="flex gap-3 bg-slate-50 p-2 rounded-lg hover:bg-brand-50 transition-colors border border-slate-100 block">
                                                        <img src={p.image_url || 'https://placehold.co/100x100'} className="w-12 h-12 object-cover rounded-md" />
                                                        <div className="flex-1 min-w-0">
                                                            <p className="text-xs font-semibold truncate">{p.title}</p>
                                                            <p className="text-xs text-brand-600 font-bold">{p.price}</p>
                                                        </div>
                                                    </Link>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                            {loading && <div className="text-slate-400 text-xs ml-4">Thinking...</div>}
                        </div>

                        <div className="p-4 bg-white border-t border-slate-100 flex gap-2">
                            <button
                                onClick={startListening}
                                className={`p-2 rounded-xl transition-colors ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
                                title="Use Voice Input"
                            >
                                {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                            </button>
                            <input
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleSend()}
                                placeholder="Ask for recommendations..."
                                className="flex-1 bg-slate-100 border-0 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-brand-500 outline-none"
                            />
                            <button onClick={() => handleSend()} disabled={loading} className="bg-slate-900 text-white px-4 py-2 rounded-xl hover:bg-slate-800 disabled:opacity-50 flex items-center gap-2 font-medium transition-colors">
                                <span>Send</span>
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    )
}
