import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, LogOut, Sparkles, LayoutGrid, FolderOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Dashboard() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [showNewProject, setShowNewProject] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProjects(response.data);
    } catch (error) {
      toast.error('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `${API}/projects`,
        { name: projectName },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Project created!');
      setShowNewProject(false);
      setProjectName("");
      navigate(`/editor/${response.data.id}`);
    } catch (error) {
      toast.error('Failed to create project');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-600" />
            <span className="text-xl font-semibold" style={{ fontFamily: 'Outfit, sans-serif' }}>A+ Generator</span>
          </div>
          <Button 
            data-testid="logout-btn"
            onClick={handleLogout} 
            variant="ghost"
            className="text-slate-600 hover:text-slate-900"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-semibold tracking-tight mb-2" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
              Your Projects
            </h1>
            <p className="text-slate-600">Create and manage your A+ content projects</p>
          </div>
          <Button 
            data-testid="new-project-btn"
            onClick={() => setShowNewProject(true)}
            className="bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-500/20"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Project
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : projects.length === 0 ? (
          <Card className="p-12 text-center border-slate-200">
            <FolderOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-xl font-medium mb-2" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
              No projects yet
            </h3>
            <p className="text-slate-600 mb-6">Create your first project to get started</p>
            <Button 
              data-testid="empty-state-create-btn"
              onClick={() => setShowNewProject(true)}
              className="bg-indigo-600 hover:bg-indigo-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              Create Project
            </Button>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Card 
                key={project.id}
                data-testid={`project-card-${project.id}`}
                className="p-6 cursor-pointer hover:shadow-xl hover:shadow-slate-200/50 transition-all border-slate-200"
                onClick={() => navigate(`/editor/${project.id}`)}
              >
                <div className="aspect-video bg-slate-100 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
                  {project.processed_image || project.original_image ? (
                    <img 
                      src={project.processed_image || project.original_image} 
                      alt={project.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <LayoutGrid className="w-12 h-12 text-slate-300" />
                  )}
                </div>
                <h3 className="text-lg font-medium mb-1" style={{ fontFamily: 'Outfit, sans-serif', color: '#0F172A' }}>
                  {project.name}
                </h3>
                <p className="text-sm text-slate-500">
                  {new Date(project.updated_at).toLocaleDateString()}
                </p>
              </Card>
            ))}
          </div>
        )}
      </main>

      <Dialog open={showNewProject} onOpenChange={setShowNewProject}>
        <DialogContent data-testid="new-project-dialog">
          <DialogHeader>
            <DialogTitle style={{ fontFamily: 'Outfit, sans-serif' }}>Create New Project</DialogTitle>
          </DialogHeader>
          <form onSubmit={createProject} className="space-y-4">
            <div>
              <Label htmlFor="project-name">Project Name</Label>
              <Input
                id="project-name"
                data-testid="project-name-input"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g., Premium Watch A+ Content"
                required
                className="mt-1"
              />
            </div>
            <Button 
              type="submit" 
              data-testid="create-project-submit-btn"
              className="w-full bg-indigo-600 hover:bg-indigo-700"
            >
              Create Project
            </Button>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}