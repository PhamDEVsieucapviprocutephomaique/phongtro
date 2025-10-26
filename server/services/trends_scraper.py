# services/trends_scraper.py
from pytrends.request import TrendReq
import pandas as pd
from typing import List, Dict, Optional
import time
import random
from datetime import datetime, timedelta

class GoogleTrendsScraper:
    def __init__(self, use_proxies=False):
        """
        Args:
            use_proxies: Nếu True, sử dụng proxy để tránh rate limit
        """
        self.use_proxies = use_proxies
        self.pytrends = self._create_pytrends_client()
        self.max_retries = 5
        self.base_delay = 2  # seconds
    
    def _create_pytrends_client(self):
        """Tạo pytrends client với hoặc không có proxy"""
        proxies = None
        if self.use_proxies:
            # Thêm proxy của bạn vào đây
            # proxies = ['http://proxy1:port', 'http://proxy2:port']
            pass
        
        return TrendReq(
            hl='vi-VN',
            tz=420,
            timeout=(10, 25)
        )
    
    def _exponential_backoff(self, attempt: int):
        """Exponential backoff với jitter"""
        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
        max_delay = 60  # Tối đa 60 giây
        return min(delay, max_delay)
    
    def _safe_request(self, func, *args, **kwargs):
        """Wrapper để retry request với exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                # Delay trước mỗi request để tránh rate limit
                if attempt > 0:
                    delay = self._exponential_backoff(attempt)
                    print(f"⏳ Retry {attempt}/{self.max_retries} - Đợi {delay:.1f}s...")
                    time.sleep(delay)
                else:
                    # Delay ngẫu nhiên 2-5 giây cho request đầu tiên
                    time.sleep(random.uniform(2, 5))
                
                result = func(*args, **kwargs)
                return result
                
            except Exception as e:
                error_msg = str(e)
                
                if "429" in error_msg or "Too Many Requests" in error_msg:
                    if attempt < self.max_retries - 1:
                        print(f"⚠️ Rate limit hit (429) - Retry {attempt + 1}/{self.max_retries}")
                        continue
                    else:
                        print(f"❌ Đã vượt quá số lần retry. Vui lòng đợi 5-10 phút và thử lại.")
                        return None
                
                elif "400" in error_msg:
                    print(f"❌ Bad request (400) - Kiểm tra lại parameters")
                    return None
                
                else:
                    print(f"❌ Lỗi: {error_msg}")
                    if attempt < self.max_retries - 1:
                        continue
                    return None
        
        return None
    
    def get_coffee_trends_24h(self) -> List[Dict]:
        """Lấy dữ liệu Google Trends về cà phê tại Việt Nam trong 24h qua"""
        print("📊 Đang lấy trends 24h...")
        
        def fetch_trends():
            # Giảm số keywords xuống 1-2 để tránh rate limit
            keywords = ['cà phê']
            
            self.pytrends.build_payload(
                kw_list=keywords,
                cat=0,
                timeframe='now 1-d',
                geo='VN',
                gprop=''
            )
            
            trends_data = self.pytrends.interest_over_time()
            
            if trends_data.empty:
                return []
            
            if 'isPartial' in trends_data.columns:
                trends_data = trends_data.drop('isPartial', axis=1)
            
            trends = []
            for idx, row in trends_data.iterrows():
                for keyword in keywords:
                    if keyword in row:
                        trends.append({
                            "timestamp": idx.strftime("%Y-%m-%d %H:%M:%S"),
                            "date": idx.strftime("%Y-%m-%d"),
                            "hour": idx.strftime("%H:%M"),
                            "keyword": keyword,
                            "interest_score": int(row[keyword]) if pd.notna(row[keyword]) else 0,
                            "country": "VN"
                        })
            
            return trends
        
        return self._safe_request(fetch_trends) or []
    
    def get_coffee_trends_hourly(self) -> List[Dict]:
        """Lấy trends theo giờ (4 giờ qua)"""
        print("⏰ Đang lấy hourly trends...")
        
        def fetch_hourly():
            self.pytrends.build_payload(
                kw_list=['cà phê'],
                timeframe='now 4-H',
                geo='VN',
                gprop=''
            )
            
            trends_data = self.pytrends.interest_over_time()
            
            if trends_data.empty:
                return []
            
            if 'isPartial' in trends_data.columns:
                trends_data = trends_data.drop('isPartial', axis=1)
            
            trends = []
            for idx, row in trends_data.iterrows():
                if 'cà phê' in row:
                    trends.append({
                        "timestamp": idx.strftime("%Y-%m-%d %H:%M:%S"),
                        "keyword": "cà phê",
                        "interest_score": int(row['cà phê']) if pd.notna(row['cà phê']) else 0,
                        "country": "VN"
                    })
            
            return trends
        
        return self._safe_request(fetch_hourly) or []
    
    def get_related_queries(self) -> Dict:
        """Lấy các queries liên quan đến cà phê"""
        print("🔍 Đang lấy related queries...")
        
        def fetch_related():
            self.pytrends.build_payload(
                kw_list=['cà phê'],
                geo='VN',
                timeframe='now 1-d'
            )
            
            return self.pytrends.related_queries()
        
        return self._safe_request(fetch_related) or {}
    
    def get_interest_by_region(self) -> pd.DataFrame:
        """Lấy interest theo tỉnh thành VN"""
        print("🗺️ Đang lấy regional interest...")
        
        def fetch_regional():
            self.pytrends.build_payload(
                kw_list=['cà phê'],
                geo='VN',
                timeframe='now 1-d'
            )
            
            return self.pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
        
        result = self._safe_request(fetch_regional)
        return result if result is not None else pd.DataFrame()
    
    def get_trending_searches_realtime(self) -> List[Dict]:
        """Lấy trending searches realtime tại Việt Nam"""
        print("⚡ Đang lấy realtime trends...")
        
        def fetch_realtime():
            trending_searches = self.pytrends.trending_searches(pn='vietnam')
            
            if trending_searches.empty:
                return []
            
            coffee_keywords = ['cà phê', 'cafe', 'coffee', 'caphe']
            trending = []
            
            for idx, keyword in trending_searches[0].items():
                keyword_lower = keyword.lower()
                if any(coffee_kw in keyword_lower for coffee_kw in coffee_keywords):
                    trending.append({
                        "keyword": keyword,
                        "rank": idx + 1,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return trending
        
        return self._safe_request(fetch_realtime) or []

# Test với rate limiting được cải thiện
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 KHỞI ĐỘNG GOOGLE TRENDS SCRAPER")
    print("=" * 60)
    print("\n⚠️ LƯU Ý:")
    print("  - Script sẽ tự động retry khi gặp rate limit")
    print("  - Có delay giữa các requests để tránh bị block")
    print("  - Nếu bị 429, vui lòng đợi 5-10 phút trước khi chạy lại")
    print("\n" + "=" * 60 + "\n")
    
    scraper = GoogleTrendsScraper()
    
    # 1. Lấy trends 24h
    print("\n📊 1. TRENDS 24 GIỜ QUA:")
    trends_24h = scraper.get_coffee_trends_24h()
    
    if trends_24h:
        print(f"✅ Tìm thấy {len(trends_24h)} data points")
        print("\n🔝 Top 10 data points gần nhất:")
        for i, trend in enumerate(trends_24h[-10:], 1):
            print(f"  {i}. {trend['timestamp']} - {trend['keyword']}: {trend['interest_score']}")
        
        avg_score = sum(t['interest_score'] for t in trends_24h) / len(trends_24h)
        print(f"\n📈 Average Interest Score (24h): {avg_score:.2f}")
        
        df = pd.DataFrame(trends_24h)
        df.to_csv('coffee_trends_24h.csv', index=False, encoding='utf-8-sig')
        print(f"💾 Đã lưu data vào: coffee_trends_24h.csv")
    else:
        print("❌ Không lấy được data 24h")
        print("💡 Tip: Đợi 5-10 phút và chạy lại script")
    
    # 2. Hourly trends (chỉ chạy nếu 24h thành công)
    if trends_24h:
        print("\n" + "=" * 60)
        print("⏰ 2. TRENDS THEO GIỜ (4 GIỜ QUA):")
        hourly_trends = scraper.get_coffee_trends_hourly()
        
        if hourly_trends:
            print(f"✅ Tìm thấy {len(hourly_trends)} data points")
            print("\n🔝 Top 10 data points gần nhất:")
            for i, trend in enumerate(hourly_trends[-10:], 1):
                print(f"  {i}. {trend['timestamp']}: {trend['interest_score']}")
        else:
            print("❌ Không lấy được hourly data")
    
    # 3. Related queries
    if trends_24h:
        print("\n" + "=" * 60)
        print("🔍 3. RELATED QUERIES (24H):")
        related = scraper.get_related_queries()
        
        if 'cà phê' in related:
            if related['cà phê']['top'] is not None and not related['cà phê']['top'].empty:
                print("\n🔥 Top Queries:")
                top_queries = related['cà phê']['top'].head(10)
                for idx, row in top_queries.iterrows():
                    print(f"  {idx+1}. {row['query']} - Score: {row['value']}")
            
            if related['cà phê']['rising'] is not None and not related['cà phê']['rising'].empty:
                print("\n📈 Rising Queries:")
                rising = related['cà phê']['rising'].head(5)
                for idx, row in rising.iterrows():
                    print(f"  {idx+1}. {row['query']} - Growth: {row['value']}")
    
    # 4. Regional interest
    if trends_24h:
        print("\n" + "=" * 60)
        print("🗺️ 4. INTEREST THEO TỈNH THÀNH:")
        regional = scraper.get_interest_by_region()
        
        if not regional.empty and 'cà phê' in regional.columns:
            top_regions = regional.nlargest(5, 'cà phê')
            for region, value in top_regions['cà phê'].items():
                print(f"  📍 {region}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)