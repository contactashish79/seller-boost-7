import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, Image, Layers, Zap, ArrowRight, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function LandingPage({ setToken, isAuthenticated }) {
  const navigate = useNavigate();
  const [showAuth, setShowAuth] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/signup';
      const response = await axios.post(`${API}${endpoint}`, { email, password });
      
      setToken(response.data.access_token);
      toast.success(isLogin ? 'Welcome back!' : 'Account created successfully!');
      setShowAuth(false);
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated) {
    navigate('/dashboard');
    return null;
  }

  return (
    <div className="min-h-screen bg-white">
      <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-600" />
            <span className="text-xl font-semibold" style={{ fontFamily: 'Outfit, sans-serif' }}>A+ Generator</span>
          </div>
          <Button 
            data-testid="nav-login-btn"
            onClick={() => setShowAuth(true)} 
            variant="ghost" 
            className="text-slate-600 hover:text-slate-900"
          >
            Sign In
          </Button>
        </div>
      </nav>

      <main className="pt-32 pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-50 rounded-full mb-6">
              <Sparkles className="w-4 h-4 text-indigo-600" />
              <span className="text-sm font-medium text-indigo-600 uppercase tracking-wide">AI-Powered Content</span>
            </div>
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-none mb-6" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
              Create Stunning <br />
              <span className="text-indigo-600">Amazon A+ Content</span>
            </h1>
            <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              Transform simple product photos into professional A+ content with AI. Remove backgrounds, generate lifestyle scenes, and create compelling copy—all in one place.
            </p>
            <Button 
              data-testid="hero-cta-btn"
              onClick={() => setShowAuth(true)} 
              className="bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-xl shadow-indigo-500/30 hover:shadow-indigo-500/40 hover:-translate-y-0.5 transition-all text-base px-8 py-6 h-auto rounded-lg"
            >
              Start Creating Free <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </div>

          <div className="relative mb-32">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-slate-50 rounded-3xl -z-10"></div>
            <img 
              src="https://images.unsplash.com/photo-1580744948109-b2da1320ac87?crop=entropy&cs=srgb&fm=jpg&q=85" 
              alt="Professional camera studio setup"
              className="w-full h-[500px] object-cover rounded-3xl shadow-2xl shadow-slate-200/50"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-32">
            {[
              {
                icon: Image,
                title: "Background Magic",
                description: "Instantly remove backgrounds or generate professional lifestyle scenes with AI",
                image: "https://images.unsplash.com/photo-1625860191460-10a66c7384fb?crop=entropy&cs=srgb&fm=jpg&q=85"
              },
              {
                icon: Layers,
                title: "Smart Enhancement",
                description: "Upscale and enhance product images to meet Amazon's quality standards",
                image: "https://images.unsplash.com/photo-1608384177866-0bca0d225435?crop=entropy&cs=srgb&fm=jpg&q=85"
              },
              {
                icon: Zap,
                title: "AI-Powered Copy",
                description: "Generate compelling product titles and descriptions that convert",
                image: "https://images.unsplash.com/photo-1759197332923-dd91f35c2b5f?crop=entropy&cs=srgb&fm=jpg&q=85"
              }
            ].map((feature, idx) => (
              <div 
                key={idx}
                data-testid={`feature-card-${idx}`}
                className="bg-white border border-slate-100 shadow-xl shadow-slate-200/40 rounded-3xl p-8 hover:shadow-2xl hover:shadow-slate-200/50 transition-all duration-300"
              >
                <div className="w-full h-48 mb-6 overflow-hidden rounded-2xl">
                  <img 
                    src={feature.image} 
                    alt={feature.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <feature.icon className="w-12 h-12 text-indigo-600 mb-4" strokeWidth={1.5} />
                <h3 className="text-2xl font-medium tracking-tight mb-3" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
                  {feature.title}
                </h3>
                <p className="text-base text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>

          <div className="bg-white border border-slate-100 shadow-xl shadow-slate-200/40 rounded-3xl p-12 text-center">
            <h2 className="text-4xl font-semibold tracking-tight mb-4" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
              Why Amazon Sellers Choose Us
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
              {[
                { label: "Time Saved", value: "80%" },
                { label: "Quality Boost", value: "2x" },
                { label: "Conversion Lift", value: "+45%" }
              ].map((stat, idx) => (
                <div key={idx}>
                  <div className="text-5xl font-bold text-indigo-600 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    {stat.value}
                  </div>
                  <div className="text-slate-600">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <Dialog open={showAuth} onOpenChange={setShowAuth}>
        <DialogContent data-testid="auth-dialog">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Outfit, sans-serif' }}>
              {isLogin ? 'Welcome Back' : 'Create Account'}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleAuth} className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                data-testid="auth-email-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                data-testid="auth-password-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-1"
              />
            </div>
            <Button 
              type="submit" 
              data-testid="auth-submit-btn"
              className="w-full bg-indigo-600 hover:bg-indigo-700"
              disabled={loading}
            >
              {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Sign Up')}
            </Button>
            <div className="text-center text-sm">
              <button
                type="button"
                data-testid="auth-toggle-btn"
                onClick={() => setIsLogin(!isLogin)}
                className="text-indigo-600 hover:text-indigo-700"
              >
                {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
              </button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}