"""
cache_manager.py
Gestor de caché para decisiones del Harness.
Memoriza decisiones entre sesiones para agentes locales.
"""
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class DecisionsCache:
    """Caché persistent de decisiones del agente"""
    
    def __init__(self, cache_dir=".opencode/memory"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "decisions_cache.json")
        self.decisions: Dict[str, Any] = {}
        self._load_cache()
    
    def _load_cache(self):
        """Carga el caché desde disco"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.decisions = data.get("decisions", {})
                print(f"[OK] Caché cargado con {len(self.decisions)} decisiones")
            except Exception as e:
                print(f"[!] Error cargando caché: {e}")
                self.decisions = {}
        else:
            self.decisions = {}
    
    def _save_cache(self):
        """Persiste el caché a disco"""
        os.makedirs(self.cache_dir, exist_ok=True)
        
        try:
            cache_data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "decision_count": len(self.decisions),
                "decisions": self.decisions
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
                print(f"[ERR] Error guardando caché: {e}")
    
    def _generate_key(self, category: str, identifier: str) -> str:
        """Genera una clave de caché única"""
        combined = f"{category}:{identifier}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def store_decision(self, category: str, identifier: str, decision: Any, 
                      metadata: Optional[Dict] = None) -> str:
        """
        Almacena una decisión en caché.
        
        Args:
            category: Categoría (ej: "file_type_to_skill", "agent_role_mapping")
            identifier: Identificador único (ej: "main.c", "developer")
            decision: La decisión/resultado a memorizar
            metadata: Metadatos opcionales (ej: timestamp, confidence)
        
        Returns:
            Clave de caché generada
        """
        key = self._generate_key(category, identifier)
        
        self.decisions[key] = {
            "category": category,
            "identifier": identifier,
            "decision": decision,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "hits": 0
        }
        
        self._save_cache()
        return key
    
    def retrieve_decision(self, category: str, identifier: str) -> Optional[Any]:
        """
        Recupera una decisión en caché.
        
        Returns:
            La decisión o None si no existe
        """
        key = self._generate_key(category, identifier)
        
        if key in self.decisions:
            entry = self.decisions[key]
            entry["hits"] += 1  # Registrar hit
            self._save_cache()
            return entry["decision"]
        
        return None
    
    def exists(self, category: str, identifier: str) -> bool:
        """Verifica si una decisión está en caché"""
        key = self._generate_key(category, identifier)
        return key in self.decisions
    
    def clear_category(self, category: str):
        """Limpia todas las decisiones de una categoría"""
        keys_to_remove = [
            key for key, entry in self.decisions.items()
            if entry.get("category") == category
        ]
        
        for key in keys_to_remove:
            del self.decisions[key]
        
        self._save_cache()
        print(f"[OK] {len(keys_to_remove)} decisiones de '{category}' eliminadas")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del caché"""
        total_decisions = len(self.decisions)
        total_hits = sum(entry.get("hits", 0) for entry in self.decisions.values())
        
        categories = {}
        for entry in self.decisions.values():
            cat = entry.get("category", "unknown")
            if cat not in categories:
                categories[cat] = {"count": 0, "hits": 0}
            categories[cat]["count"] += 1
            categories[cat]["hits"] += entry.get("hits", 0)
        
        return {
            "total_decisions": total_decisions,
            "total_hits": total_hits,
            "categories": categories,
            "cache_file_size_kb": os.path.getsize(self.cache_file) // 1024 if os.path.exists(self.cache_file) else 0
        }
    
    def print_stats(self):
        """Imprime estadísticas del caché de forma legible"""
        stats = self.get_stats()
        
        print("\n[INFO] ESTADÍSTICAS DE CACHÉ")
        print(f"   Total decisiones: {stats['total_decisions']}")
        print(f"   Total hits: {stats['total_hits']}")
        print(f"   Tamaño archivo: {stats['cache_file_size_kb']} KB")
        
        if stats['categories']:
            print("\n   Por categoría:")
            for cat, data in stats['categories'].items():
                print(f"     - {cat}: {data['count']} decisiones, {data['hits']} hits")


class ContextWindowTracker:
    """Rastrea y optimiza el uso de context window"""
    
    def __init__(self, cache_dir=".opencode/memory"):
        self.cache_dir = cache_dir
        self.tracker_file = os.path.join(cache_dir, "context_window_track.json")
        self.snapshots: list = []
        self._load_snapshots()
    
    def _load_snapshots(self):
        """Carga snapshots previos"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    self.snapshots = json.load(f)
            except:
                self.snapshots = []
    
    def _save_snapshots(self):
        """Persiste snapshots"""
        os.makedirs(self.cache_dir, exist_ok=True)
        
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.snapshots, f, indent=2)
        except Exception as e:
            print(f"❌ Error guardando snapshots: {e}")
    
    def record_snapshot(self, description: str, metrics: Dict[str, Any]):
        """
        Registra un snapshot de uso de context window.
        
        Args:
            description: Descripción del estado (ej: "Initial load", "After lazy-loading")
            metrics: Dict con métricas (ej: {"tokens": 1024, "kb": 45})
        """
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "metrics": metrics
        }
        
        self.snapshots.append(snapshot)
        self._save_snapshots()
    
    def compare_snapshots(self, idx1: int = 0, idx2: int = -1) -> Dict[str, Any]:
        """
        Compara dos snapshots para medir mejoras.
        
        Args:
            idx1: Índice del primer snapshot
            idx2: Índice del segundo snapshot
        
        Returns:
            Dict con comparativa
        """
        if len(self.snapshots) < 2:
            return {"error": "No hay suficientes snapshots"}
        
        snap1 = self.snapshots[idx1]
        snap2 = self.snapshots[idx2]
        
        metrics1 = snap1.get("metrics", {})
        metrics2 = snap2.get("metrics", {})
        
        comparison = {
            "before": snap1["description"],
            "after": snap2["description"],
            "improvements": {}
        }
        
        # Comparar métricas numéricas
        for key in metrics1.keys():
            if key in metrics2:
                val1 = metrics1[key]
                val2 = metrics2[key]
                
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    diff = val1 - val2
                    percent = round((diff / val1 * 100) if val1 > 0 else 0, 1)
                    
                    comparison["improvements"][key] = {
                        "before": val1,
                        "after": val2,
                        "reduction": diff,
                        "percent": percent
                    }
        
        return comparison


__all__ = ['DecisionsCache', 'ContextWindowTracker']
