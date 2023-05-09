//
//  JSONManager.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 7/5/2023.
//

import Foundation

struct Product: Codable {
    let shopName: String
    let address: Address
    
    static let allProducts: [Product] = Bundle.main.decode(file: "example.json")
    static let sampleProduct: Product = allProducts[0]
}

struct Address: Codable {
    let streetAddress: String
    let suburb: String?
    let state, postcode: String
    let city: String?
}

extension Bundle {
    func decode<T: Decodable>(file: String) -> T {
        guard let url = self.url(forResource: file, withExtension: nil) else {
            fatalError("Could not find file \(file)")
        }
        
        guard let data = try? Data(contentsOf: url) else {
            fatalError("Could not load file \(file)")
        }
        
        let decoder = JSONDecoder()
        
        guard let loadedData = try? decoder.decode(T.self, from: data) else {
            fatalError("Could not decode data")
        }
        
        return loadedData
    }
}
