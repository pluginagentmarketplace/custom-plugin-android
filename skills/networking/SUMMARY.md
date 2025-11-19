# Networking & APIs - Android Development Agent
## Comprehensive Documentation Summary

### Overview
Bu belge, Android geliştirmesinde Networking ve APIs konusunda kapsamlı bir rehber sunar. Retrofit, OkHttp, REST APIs, JSON ve ilgili teknolojilerin detaylı açıklamaları, kod örnekleri ve best practices içerir.

---

## Dosya Yapısı

```
/home/user/custom-plugin-android/skills/networking/
├── networking-apis.md           # 1101 satır detaylı belgelendirme
├── networking-apis.json         # Yapılandırılmış veri (JSON formatında)
├── agent-definition.yaml        # Agent tanımı ve yetenekleri
└── SUMMARY.md                   # Bu dosya
```

---

## Agent Özellikleri

### Description
Android uygulamalarında HTTP istek/yanıt yönetimi, REST API entegrasyonu, JSON veri işleme ve ağ iletişimi için kapsamlı rehber. Retrofit, OkHttp gibi modern kütüphanelerle verimli API haberleşmesi, hata yönetimi, güvenlik ve performans optimizasyonu.

### Capabilities (14 Ana Yetenek)
1. **REST API tasarımı ve tüketimi**
2. **HTTP istek/yanıt yönetimi**
3. **JSON veri serileştirme/deserileştirme**
4. **Retrofit ile type-safe API tanımları**
5. **OkHttp konfigürasyonu ve interceptor'ları**
6. **Hata yönetimi ve retry stratejileri**
7. **SSL/TLS ve güvenlik ayarları**
8. **Ağ bağlantı durumu kontrol etme**
9. **Veri sıkıştırma ve performans optimizasyonu**
10. **Mock server'lar ile test etme**
11. **Pagination ve veri akışı yönetimi**
12. **File upload/download operasyonları**
13. **Token yönetimi ve Bearer authentication**
14. **Network monitoring ve connectivity tracking**

---

## Ana Konular (9 Bölüm)

### 1. REST APIs Temelleri
- HTTP Metotları (GET, POST, PUT, PATCH, DELETE)
- HTTP Durum Kodları (2xx, 3xx, 4xx, 5xx)
- API Design Best Practices
- Endpoint Tasarımı ve Query Parameters

### 2. JSON - JavaScript Object Notation
- JSON Veri Yapısı ve Tipleri
- Manual Parsing (JSONObject, JSONArray)
- GSON Serileştirmesi
- Moshi Type-Safe Processing

### 3. OkHttp - HTTP İstemci
- Temel Kurulumu ve Konfigürasyonu
- GET/POST İstekleri
- Interceptor Oluşturma (Logging, Auth, Connectivity)
- Timeout ve Retry Politikaları
- Connection Pooling

### 4. Retrofit - Type-Safe HTTP Framework
- API Interface Tanımı
- Anotasyonlar (@GET, @POST, @PUT, @DELETE)
- Parametreler (@Path, @Query, @Header, @Body)
- Multipart File Upload
- Call Adapters (Coroutine, RxJava, LiveData, Flow)
- Error Handling Patterns

### 5. Ağ Bağlantı Yönetimi
- Bağlantı Durumu Kontrol Etme
- WiFi/Cellular Durumu Tespiti
- Network Callbacks
- Connectivity Interceptor
- Offline Mode Desteği

### 6. Güvenlik (Security)
- SSL/TLS Konfigürasyonu
- Certificate Pinning
- Token Yönetimi
- Bearer Token Interceptor
- JWT (JSON Web Token)
- Encrypted SharedPreferences

### 7. İleri Konular
- Pagination Implementasyonu
- File Upload/Download
- Request/Response Interceptors
- Caching Stratejileri
- Rate Limiting
- Data Compression

### 8. Testing
- MockWebServer ile Unit Testing
- Mock API Response'ları
- Repository Testing
- Network Failure Scenarios
- Integration Testing

### 9. Praktik Örnekler
- Complete API Integration Flow
- MVVM Architektürü
- Error Handling Best Practices
- Logging ve Debugging

---

## Öğrenme Saati Dağılımı

### Başlangıç (Beginner)
- **Süresi:** 20 saat
- **Konular:**
  - REST API Temelleri
  - JSON Temel İşleme
  - OkHttp Basit Kullanımı
  - Retrofit Temel Kurulumu
  - Basit GET/POST İstekleri

### Orta Seviye (Intermediate)
- **Süresi:** 30 saat
- **Konular:**
  - Advanced Interceptors
  - Error Handling Patterns
  - Pagination Implementasyonu
  - Token Management
  - Network Monitoring
  - File Upload/Download

### İleri Seviye (Advanced)
- **Süresi:** 25 saat
- **Konular:**
  - SSL/TLS Security
  - Certificate Pinning
  - Custom Call Adapters
  - Advanced Caching
  - Performance Optimization
  - Comprehensive Testing

**TOPLAM: 75 Saat**

---

## Gerekli Bağımlılıklar

```gradle
dependencies {
    // Retrofit
    implementation 'com.squareup.retrofit2:retrofit:2.10.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.10.0'
    implementation 'com.squareup.retrofit2:converter-moshi:2.10.0'

    // OkHttp
    implementation 'com.squareup.okhttp3:okhttp:4.11.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'

    // JSON Processing
    implementation 'com.google.code.gson:gson:2.10.1'
    implementation 'com.squareup.moshi:moshi-kotlin:1.15.0'

    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3'

    // Security
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'

    // Testing
    testImplementation 'com.squareup.okhttp3:mockwebserver:4.11.0'
    testImplementation 'io.mockk:mockk:1.13.5'
}
```

---

## Best Practices (14 Madde)

1. ✅ Her zaman type-safe API interfaces kullanın (Retrofit)
2. ✅ Interceptor'lar ile centralized request/response handling yapın
3. ✅ Timeout değerlerini mantıklı şekilde ayarlayın (30+ saniye)
4. ✅ Token'ları EncryptedSharedPreferences'de saklayın
5. ✅ Bağlantı durumunu kontrol edip offline mode'u destekleyin
6. ✅ Network işlemlerini IO Dispatcher'da çalıştırın
7. ✅ Error handling için sealed class pattern kullanın
8. ✅ SSL/TLS certificate pinning implementasyonu yapın
9. ✅ Logging interceptor'ını production'da disable edin
10. ✅ Mock server'lar ile comprehensive test coverage sağlayın
11. ✅ Request/response sürelerini monitor edin
12. ✅ Pagination için cursor-based yaklaşımı tercih edin
13. ✅ File transfer'lar için progress callback'ler ekleyin
14. ✅ Rate limiting'i göz önünde bulundurun

---

## Sık Hatalar (10 Madde)

❌ Main thread'de network işlemleri yapmak
❌ Timeout değerlerini çok düşük ayarlamak
❌ Error response body'sini okuyor olmak
❌ Token refresh'i doğru implemente etmemek
❌ Interceptor'larda exception handling'i unutmak
❌ Connection pool'u düzgün konfigüre etmemek
❌ Mock response'ları production'da bırakmak
❌ Memory leak'ler için Retrofit lifecycle'ını yönetmemek
❌ SSL/TLS pinning'i implement etmemek
❌ Network errors'ı user'a göstermemek

---

## Praktik Projeler (5 Adet)

### 1. Weather App (Beginner)
- **Açıklama:** OpenWeather API ile hava durumu uygulaması
- **Anahtar Konseptler:** GET requests, JSON parsing, Error handling

### 2. Social Media Feed (Intermediate)
- **Açıklama:** Paginated list ile sosyal medya feed uygulaması
- **Anahtar Konseptler:** Pagination, Caching, Refreshing

### 3. User Authentication System (Intermediate)
- **Açıklama:** Token-based authentication ile login/register sistemi
- **Anahtar Konseptler:** Token management, Interceptors, Refresh tokens

### 4. File Upload Service (Advanced)
- **Açıklama:** Multipart file upload ve progress tracking
- **Anahtar Konseptler:** Multipart requests, Progress callbacks, Resumable uploads

### 5. Real-time Chat App (Advanced)
- **Açıklama:** WebSocket ve REST API kombinasyonu ile chat uygulaması
- **Anahtar Konseptler:** WebSocket, Message queuing, Offline support

---

## Kod Örnekleri Özeti

Belge içerisinde aşağıdaki kod örnekleri yer almaktadır:

### OkHttp Örnekleri
- Basit GET isteği
- POST isteği with JSON body
- Logging Interceptor
- Custom Interceptor (Bearer Token)
- OkHttp Konfigürasyonu
- Error Handling

### Retrofit Örnekleri
- API Interface Tanımı
- CRUD Operasyonları
- Retrofit Builder
- Coroutine Entegrasyonu
- Error Handling Patterns
- Call Adapters

### JSON Örnekleri
- JSONObject ile manual parsing
- JSONArray işleme
- GSON serileştirmesi/deserileştirmesi
- Moshi kullanımı
- Custom JSON deserializers

### Ağ Yönetimi
- Bağlantı durumu kontrolü
- Network Callbacks
- Connectivity Interceptor
- Network Monitoring

### Güvenlik Örnekleri
- SSL/TLS Konfigürasyonu
- Token Yönetimi
- Bearer Token Interceptor
- Encrypted SharedPreferences

### Testing Örnekleri
- MockWebServer Setup
- Mock Responses
- Repository Testing
- Error Scenarios

---

## Kaynaklar

- [Retrofit Documentation](https://square.github.io/retrofit/)
- [OkHttp Documentation](https://square.github.io/okhttp/)
- [Android Networking Best Practices](https://developer.android.com/training/connect-devices-wirelessly/network-ops)
- [JSON in Android](https://developer.android.com/guide/topics/data/data-storage)
- [HTTP Protocol Specifications](https://tools.ietf.org/html/rfc7231)

---

## Dosya Bilgileri

| Dosya | Satır/Boyut | Açıklama |
|-------|------------|---------|
| networking-apis.md | 1101 satır | Detaylı belgelendirme, kod örnekleri |
| networking-apis.json | 9143 byte | Yapılandırılmış veri formatı |
| agent-definition.yaml | YAML format | Agent tanımı ve yetenekleri |
| SUMMARY.md | Bu dosya | Özet ve rehber |

---

## Başlangıç Rehberi

### Adım 1: Temel Kavramları Öğrenin
1. REST API temellerini anlamak
2. JSON veri formatını öğrenmek
3. HTTP protokolünü incelemek

### Adım 2: Araçları Kurun
1. Retrofit ve OkHttp bağımlılıklarını eklemek
2. Android Studio'da projeyi konfigüre etmek
3. Postman ile API testing'i öğrenmek

### Adım 3: Basit Örneklerle Başlayın
1. Basit GET isteği yapmak
2. JSON parse etmek
3. Retrofit API interface'i tanımlamak

### Adım 4: İleri Konulara Geçin
1. Error handling implementasyonu
2. Token yönetimi
3. Network security

### Adım 5: Test Yazın
1. MockWebServer ile test etmek
2. Integration test'ler yazmak
3. Error scenario'ları test etmek

---

## Sertifikasyon Yolu

1. **Basic Networking Fundamentals** ← Başlangıç
2. **API Integration Specialist** ← Orta Seviye
3. **Advanced Network Architecture** ← İleri Seviye
4. **Android Networking Expert** ← Master Seviye

---

## Başarı Kriterleri

- ✅ Retrofit API interfaces doğru yazabilmek
- ✅ OkHttp interceptor'ları implement edebilmek
- ✅ JSON veri işlemesini yapabilmek
- ✅ Error handling ve retry logic yazabilmek
- ✅ Network security uygulamalarını implement edebilmek
- ✅ Uygun unit testler yazabilmek

---

## Son Notlar

Bu belge, Android geliştirmesinde Networking ve APIs konusunda kapsamlı bir rehber olarak hazırlanmıştır. Tüm kod örnekleri production-ready ve best practices'i takip etmektedir.

Her seviyedeki geliştirici için uygun öğrenme materyali içermektedir. Başlangıç seviyesinden başlayarak ileri seviyelere doğru ilerleyebilirsiniz.

**Başarılar dileriz! 🚀**

---

*Son güncelleme: 2025-11-18*
*Versiyon: 1.0.0*
