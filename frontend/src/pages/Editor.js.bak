import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Upload, Sparkles, Scissors, Layers, Zap, Download, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Editor() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const token = localStorage.getItem('token');

  const [project, setProject] = useState(null);
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [aiTitle, setAiTitle] = useState("");
  const [aiDescription, setAiDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeOperation, setActiveOperation] = useState("");

  const [bgPrompt, setBgPrompt] = useState("");
  const [productType, setProductType] = useState("");
  const [keyFeatures, setKeyFeatures] = useState("");

  useEffect(() => {
    if (projectId) {
      loadProject();
    }
  }, [projectId]);

  const loadProject = async () => {
    try {
      const response = await axios.get(`${API}/projects/${projectId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const proj = response.data;
      setProject(proj);
      if (proj.original_image) setOriginalImage(proj.original_image);
      if (proj.processed_image) setProcessedImage(proj.processed_image);
      if (proj.ai_title) setAiTitle(proj.ai_title);
      if (proj.ai_description) setAiDescription(proj.ai_description);
    } catch (error) {
      toast.error('Failed to load project');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setActiveOperation('upload');
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API}/image/upload`, formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setOriginalImage(response.data.image);
      setProcessedImage(response.data.image);
      toast.success('Image uploaded!');

      if (projectId) {
        await axios.put(
          `${API}/projects/${projectId}`,
          { original_image: response.data.image, processed_image: response.data.image },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
    } catch (error) {
      toast.error('Upload failed');
    } finally {
      setLoading(false);
      setActiveOperation('');
    }
  };

  const handleRemoveBackground = async () => {
    if (!processedImage) {
      toast.error('Please upload an image first');
      return;
    }

    setLoading(true);
    setActiveOperation('remove-bg');
    try {
      const response = await axios.post(
        `${API}/image/remove-background`,
        { image: processedImage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setProcessedImage(response.data.image);
      toast.success('Background removed!');

      if (projectId) {
        await axios.put(
          `${API}/projects/${projectId}`,
          { processed_image: response.data.image },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
    } catch (error) {
      toast.error('Background removal failed');
    } finally {
      setLoading(false);
      setActiveOperation('');
    }
  };

  const handleGenerateBackground = async () => {
    if (!processedImage || !bgPrompt) {
      toast.error('Please upload an image and enter a background prompt');
      return;
    }

    setLoading(true);
    setActiveOperation('gen-bg');
    try {
      const response = await axios.post(
        `${API}/image/generate-background`,
        { prompt: bgPrompt, reference_image: processedImage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setProcessedImage(response.data.image);
      toast.success('Background generated!');
      setBgPrompt("");

      if (projectId) {
        await axios.put(
          `${API}/projects/${projectId}`,
          { processed_image: response.data.image },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Background generation failed');
    } finally {
      setLoading(false);
      setActiveOperation('');
    }
  };

  const handleEnhance = async () => {
    if (!processedImage) {
      toast.error('Please upload an image first');
      return;
    }

    setLoading(true);
    setActiveOperation('enhance');
    try {
      const response = await axios.post(
        `${API}/image/enhance`,
        { image: processedImage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setProcessedImage(response.data.image);
      toast.success('Image enhanced!');

      if (projectId) {
        await axios.put(
          `${API}/projects/${projectId}`,
          { processed_image: response.data.image },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
    } catch (error) {
      toast.error('Enhancement failed');
    } finally {
      setLoading(false);
      setActiveOperation('');
    }
  };

  const handleGenerateContent = async () => {
    if (!productType) {
      toast.error('Please enter a product type');
      return;
    }

    setLoading(true);
    setActiveOperation('gen-content');
    try {
      const response = await axios.post(
        `${API}/content/generate`,
        { product_type: productType, key_features: keyFeatures },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setAiTitle(response.data.title);
      setAiDescription(response.data.description);
      toast.success('Content generated!');

      if (projectId) {
        await axios.put(
          `${API}/projects/${projectId}`,
          { ai_title: response.data.title, ai_description: response.data.description },
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Content generation failed');
    } finally {
      setLoading(false);
      setActiveOperation('');
    }
  };

  const handleDownload = () => {
    if (!processedImage) {
      toast.error('No image to download');
      return;
    }

    const link = document.createElement('a');
    link.href = processedImage;
    link.download = `${project?.name || 'image'}.png`;
    link.click();
    toast.success('Image downloaded!');
  };

  const handleSave = async () => {
    if (!projectId) return;

    try {
      await axios.put(
        `${API}/projects/${projectId}`,
        {
          processed_image: processedImage,
          ai_title: aiTitle,
          ai_description: aiDescription
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Project saved!');
    } catch (error) {
      toast.error('Save failed');
    }
  };

  return (
    <div className="h-screen flex flex-col bg-white">
      <nav className="bg-white border-b border-slate-200 h-16 flex items-center px-4 gap-4">
        <Button 
          data-testid="back-to-dashboard-btn"
          onClick={() => navigate('/dashboard')} 
          variant="ghost" 
          size="sm"
          className="text-slate-600"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <div className="flex-1">
          <h1 className="text-lg font-semibold" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
            {project?.name || 'New Project'}
          </h1>
        </div>
        <Button 
          data-testid="save-project-btn"
          onClick={handleSave} 
          variant="ghost" 
          size="sm"
          className="text-slate-600"
        >
          <Save className="w-4 h-4 mr-2" />
          Save
        </Button>
      </nav>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-[320px_1fr_380px] overflow-hidden">
        <div className="bg-slate-50 border-r border-slate-200 p-4 overflow-y-auto">
          <h2 className="text-lg font-semibold mb-4" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
            Tools
          </h2>

          <div className="space-y-3">
            <Card className="p-4 border-slate-200">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
              <Button
                data-testid="upload-image-btn"
                onClick={() => fileInputRef.current?.click()}
                className="w-full bg-indigo-600 hover:bg-indigo-700"
                disabled={loading}
              >
                <Upload className="w-4 h-4 mr-2" />
                {activeOperation === 'upload' ? 'Uploading...' : 'Upload Image'}
              </Button>
            </Card>

            <Card className="p-4 border-slate-200">
              <h3 className="font-medium mb-3 text-sm" style={{ fontFamily: 'Outfit, sans-serif' }}>Remove Background</h3>
              <Button
                data-testid="remove-bg-btn"
                onClick={handleRemoveBackground}
                className="w-full"
                variant="secondary"
                disabled={loading || !processedImage}
              >
                <Scissors className="w-4 h-4 mr-2" />
                {activeOperation === 'remove-bg' ? 'Processing...' : 'Remove BG'}
              </Button>
            </Card>

            <Card className="p-4 border-slate-200">
              <h3 className="font-medium mb-3 text-sm" style={{ fontFamily: 'Outfit, sans-serif' }}>Generate Background</h3>
              <Input
                data-testid="bg-prompt-input"
                placeholder="e.g., luxury marble table"
                value={bgPrompt}
                onChange={(e) => setBgPrompt(e.target.value)}
                className="mb-2"
              />
              <Button
                data-testid="generate-bg-btn"
                onClick={handleGenerateBackground}
                className="w-full"
                variant="secondary"
                disabled={loading || !processedImage || !bgPrompt}
              >
                <Sparkles className="w-4 h-4 mr-2" />
                {activeOperation === 'gen-bg' ? 'Generating...' : 'Generate'}
              </Button>
            </Card>

            <Card className="p-4 border-slate-200">
              <h3 className="font-medium mb-3 text-sm" style={{ fontFamily: 'Outfit, sans-serif' }}>Enhance Image</h3>
              <Button
                data-testid="enhance-btn"
                onClick={handleEnhance}
                className="w-full"
                variant="secondary"
                disabled={loading || !processedImage}
              >
                <Layers className="w-4 h-4 mr-2" />
                {activeOperation === 'enhance' ? 'Enhancing...' : 'Enhance'}
              </Button>
            </Card>
          </div>
        </div>

        <div className="bg-slate-100/50 p-8 flex items-center justify-center relative overflow-hidden pattern-grid-lg">
          <div data-testid="image-canvas" className="max-w-3xl w-full">
            {processedImage ? (
              <div className="bg-white rounded-2xl shadow-2xl p-4">
                <img 
                  src={processedImage} 
                  alt="Product"
                  className="w-full h-auto rounded-lg"
                />
                <div className="mt-4 flex gap-2">
                  <Button
                    data-testid="download-image-btn"
                    onClick={handleDownload}
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-2xl border-2 border-dashed border-slate-300 p-16 text-center">
                <Upload className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                <p className="text-slate-500">Upload an image to get started</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white border-l border-slate-200 p-4 overflow-y-auto">
          <h2 className="text-lg font-semibold mb-4" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
            AI Content
          </h2>

          <Card className="p-4 mb-4 border-slate-200">
            <h3 className="font-medium mb-3 text-sm" style={{ fontFamily: 'Outfit, sans-serif' }}>Generate A+ Copy</h3>
            <div className="space-y-2 mb-3">
              <Input
                data-testid="product-type-input"
                placeholder="Product type (e.g., Wireless Headphones)"
                value={productType}
                onChange={(e) => setProductType(e.target.value)}
              />
              <Textarea
                data-testid="key-features-input"
                placeholder="Key features (optional)"
                value={keyFeatures}
                onChange={(e) => setKeyFeatures(e.target.value)}
                rows={3}
              />
            </div>
            <Button
              data-testid="generate-content-btn"
              onClick={handleGenerateContent}
              className="w-full bg-indigo-600 hover:bg-indigo-700"
              disabled={loading || !productType}
            >
              <Zap className="w-4 h-4 mr-2" />
              {activeOperation === 'gen-content' ? 'Generating...' : 'Generate Copy'}
            </Button>
          </Card>

          {(aiTitle || aiDescription) && (
            <Card className="p-4 border-slate-200">
              <div className="space-y-4">
                <div>
                  <Label className="text-sm font-medium mb-1 block">Title</Label>
                  <Textarea
                    data-testid="ai-title-textarea"
                    value={aiTitle}
                    onChange={(e) => setAiTitle(e.target.value)}
                    rows={2}
                    className="text-sm"
                  />
                </div>
                <div>
                  <Label className="text-sm font-medium mb-1 block">Description</Label>
                  <Textarea
                    data-testid="ai-description-textarea"
                    value={aiDescription}
                    onChange={(e) => setAiDescription(e.target.value)}
                    rows={8}
                    className="text-sm"
                  />
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}