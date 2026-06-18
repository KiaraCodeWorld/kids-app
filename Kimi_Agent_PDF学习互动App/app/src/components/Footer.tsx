import { Rocket } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#2C3E50] py-6 px-4 text-center">
      <p className="text-white/60 text-sm flex items-center justify-center gap-1" style={{ fontFamily: 'Nunito, sans-serif' }}>
        Math Quest — Making math fun, one problem at a time! <Rocket className="w-4 h-4 text-[#FF6B35]" />
      </p>
    </footer>
  );
}
