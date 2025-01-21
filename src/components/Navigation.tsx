import { Twitter } from 'lucide-react';

const Navigation = () => {
  return (
    <nav className="fixed bottom-4 left-0 w-full border-t border-white/20 bg-black/80 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-1.5 flex justify-between items-center">
        <div className="text-white/60 text-sm">NEVERA Terminal v1.0.0</div>
        <a
          href="https://twitter.com"
          target="_blank"
          rel="noopener noreferrer"
          className="text-white/60 hover:text-white transition-colors"
        >
          <Twitter className="w-5 h-5" />
        </a>
      </div>
    </nav>
  );
};

export default Navigation;