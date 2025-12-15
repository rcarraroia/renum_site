/**
 * Cache Manager for managing application-wide cache
 * Provides cache invalidation strategies and cache synchronization
 */

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresAt: number;
}

interface CacheConfig {
  defaultTTL?: number; // Time to live in milliseconds
  maxSize?: number; // Maximum number of entries
}

class CacheManager {
  private cache: Map<string, CacheEntry<any>>;
  private config: Required<CacheConfig>;
  private subscribers: Map<string, Set<(data: any) => void>>;

  constructor(config: CacheConfig = {}) {
    this.cache = new Map();
    this.config = {
      defaultTTL: config.defaultTTL || 5 * 60 * 1000, // 5 minutes default
      maxSize: config.maxSize || 100,
    };
    this.subscribers = new Map();
  }

  /**
   * Get data from cache
   */
  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }

    // Check if expired
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return null;
    }

    return entry.data as T;
  }

  /**
   * Set data in cache
   */
  set<T>(key: string, data: T, ttl?: number): void {
    const timestamp = Date.now();
    const expiresAt = timestamp + (ttl || this.config.defaultTTL);

    // Enforce max size
    if (this.cache.size >= this.config.maxSize) {
      // Remove oldest entry
      const oldestKey = Array.from(this.cache.entries())
        .sort((a, b) => a[1].timestamp - b[1].timestamp)[0][0];
      this.cache.delete(oldestKey);
    }

    this.cache.set(key, { data, timestamp, expiresAt });

    // Notify subscribers
    this.notifySubscribers(key, data);
  }

  /**
   * Invalidate specific cache entry
   */
  invalidate(key: string): void {
    this.cache.delete(key);
    this.notifySubscribers(key, null);
  }

  /**
   * Invalidate cache entries matching a pattern
   */
  invalidatePattern(pattern: string | RegExp): void {
    const regex = typeof pattern === 'string' 
      ? new RegExp(pattern) 
      : pattern;

    const keysToDelete: string[] = [];
    
    this.cache.forEach((_, key) => {
      if (regex.test(key)) {
        keysToDelete.push(key);
      }
    });

    keysToDelete.forEach(key => {
      this.cache.delete(key);
      this.notifySubscribers(key, null);
    });
  }

  /**
   * Invalidate all cache entries for a resource type
   */
  invalidateResource(resource: string): void {
    this.invalidatePattern(`^${resource}`);
  }

  /**
   * Clear all cache
   */
  clear(): void {
    this.cache.clear();
    this.subscribers.forEach((subscribers, key) => {
      subscribers.forEach(callback => callback(null));
    });
  }

  /**
   * Subscribe to cache changes for a specific key
   */
  subscribe(key: string, callback: (data: any) => void): () => void {
    if (!this.subscribers.has(key)) {
      this.subscribers.set(key, new Set());
    }

    this.subscribers.get(key)!.add(callback);

    // Return unsubscribe function
    return () => {
      const subscribers = this.subscribers.get(key);
      if (subscribers) {
        subscribers.delete(callback);
        if (subscribers.size === 0) {
          this.subscribers.delete(key);
        }
      }
    };
  }

  /**
   * Notify all subscribers of a key
   */
  private notifySubscribers(key: string, data: any): void {
    const subscribers = this.subscribers.get(key);
    if (subscribers) {
      subscribers.forEach(callback => callback(data));
    }
  }

  /**
   * Get cache statistics
   */
  getStats() {
    const now = Date.now();
    let expired = 0;
    let active = 0;

    this.cache.forEach(entry => {
      if (now > entry.expiresAt) {
        expired++;
      } else {
        active++;
      }
    });

    return {
      total: this.cache.size,
      active,
      expired,
      maxSize: this.config.maxSize,
      subscribers: this.subscribers.size,
    };
  }

  /**
   * Clean up expired entries
   */
  cleanup(): void {
    const now = Date.now();
    const keysToDelete: string[] = [];

    this.cache.forEach((entry, key) => {
      if (now > entry.expiresAt) {
        keysToDelete.push(key);
      }
    });

    keysToDelete.forEach(key => this.cache.delete(key));
  }
}

// Create singleton instance
export const cacheManager = new CacheManager({
  defaultTTL: 5 * 60 * 1000, // 5 minutes
  maxSize: 100,
});

// Auto cleanup every minute
setInterval(() => {
  cacheManager.cleanup();
}, 60 * 1000);

export default cacheManager;
