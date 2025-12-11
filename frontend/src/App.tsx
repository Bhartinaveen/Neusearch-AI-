import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import ProductDetail from './pages/ProductDetail'
import Navbar from './components/Navbar'
import ChatInterface from './components/ChatInterface'

import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col">
      <Navbar />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/product/:id" element={<ProductDetail />} />
        </Routes>
      </main>
      <Footer />
      <ChatInterface />
    </div>
  )
}

export default App
